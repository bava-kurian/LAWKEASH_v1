import { NextResponse } from 'next/server';

export async function POST(req: Request) {
    try {
        const body = await req.json();
        const { question } = body;

        // Default to localhost:8000 if not specified
        const backendUrl = process.env.BACKEND_URL || 'http://127.0.0.1:8000';

        const response = await fetch(`${backendUrl}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                query: question,
                use_local: false,
            }),
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            console.error('Backend error:', response.status, errorData);
            return NextResponse.json(
                { error: 'Failed to communicate with LawKeash backend' },
                { status: response.status }
            );
        }

        const data = await response.json();

        // Parse the context_used string into structured sources
        // Format is "Source: Act: {act}, Section: {section}\nContent: {content}\n\n"
        const sources = [];
        if (data.context_used && data.context_used !== "No relevant legal context found.") {
            const contextBlocks = data.context_used.split('\n\n').filter((block: string) => block.trim().length > 0);

            for (const block of contextBlocks) {
                const sourceMatch = block.match(/Source: Act: (.*?), Section: (.*?)\nContent: (.*)/s);

                if (sourceMatch) {
                    const [_, act, section, content] = sourceMatch;
                    sources.push({
                        content: content.trim(),
                        metadata: {
                            source: `Act: ${act}, Section: ${section}`,
                            page_label: "N/A", // Backend doesn't provide page info currently
                            total_pages: 1,
                            page: 1
                        }
                    });
                }
            }
        }

        return NextResponse.json({
            answer: data.response,
            sources: sources,
        });

    } catch (error) {
        console.error('API Route Error:', error);
        return NextResponse.json(
            { error: 'Internal Server Error' },
            { status: 500 }
        );
    }
}
