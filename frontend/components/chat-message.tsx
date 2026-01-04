import { MessageCircle, FileText, ChevronDown, ChevronUp } from "lucide-react"
import ReactMarkdown from "react-markdown"
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "@/components/ui/collapsible"
import { useState } from "react"

interface MessageProps {
  message: {
    role: "user" | "assistant"
    content: string
    sources?: Array<{
      content: string
      metadata: {
        page_label: string
        total_pages: number
        source: string
        page: number
        [key: string]: any
      }
    }>
  }
}

export default function ChatMessage({ message }: MessageProps) {
  const [isOpen, setIsOpen] = useState(false)

  if (message.role === "user") {
    return (
      <div className="flex justify-end">
        <div className="max-w-2xl rounded-lg bg-primary px-4 py-3 text-primary-foreground">
          <p className="text-sm">{message.content}</p>
        </div>
      </div>
    )
  }

  return (
    <div className="flex justify-start">
      <div className="max-w-2xl space-y-4">
        <div className="flex gap-3">
          <div className="mt-1 rounded-lg bg-accent/20 p-2">
            <MessageCircle className="h-4 w-4 text-accent" />
          </div>
          <div className="flex-1 rounded-lg bg-card border border-border px-4 py-3">
            <div className="text-sm leading-relaxed text-foreground prose prose-sm dark:prose-invert max-w-none">
              <ReactMarkdown
                components={{
                  p: ({ children }: { children: React.ReactNode }) => <p className="mb-2 last:mb-0">{children}</p>,
                  ul: ({ children }: { children: React.ReactNode }) => <ul className="list-disc pl-4 mb-2">{children}</ul>,
                  ol: ({ children }: { children: React.ReactNode }) => <ol className="list-decimal pl-4 mb-2">{children}</ol>,
                  li: ({ children }: { children: React.ReactNode }) => <li className="mb-1">{children}</li>,
                  strong: ({ children }: { children: React.ReactNode }) => <span className="font-bold text-primary">{children}</span>,
                  a: ({ href, children }: { href?: string; children: React.ReactNode }) => (
                    <a href={href} target="_blank" rel="noopener noreferrer" className="text-primary hover:underline">
                      {children}
                    </a>
                  ),
                }}
              >
                {message.content}
              </ReactMarkdown>
            </div>
          </div>
        </div>

        {message.sources && message.sources.length > 0 && (
          <div className="ml-11">
            <Collapsible open={isOpen} onOpenChange={setIsOpen} className="space-y-2">
              <CollapsibleTrigger asChild>
                <button className="flex items-center gap-2 text-xs font-semibold uppercase text-muted-foreground hover:text-foreground transition-colors">
                  <span>{isOpen ? "Hide Sources" : `View ${message.sources.length} Sources`}</span>
                  {isOpen ? <ChevronUp className="h-3 w-3" /> : <ChevronDown className="h-3 w-3" />}
                </button>
              </CollapsibleTrigger>
              <CollapsibleContent className="space-y-2 animate-slide-in">
                {message.sources.map((source, idx) => (
                  <div
                    key={idx}
                    className="rounded-lg border border-border/50 bg-card/50 p-3 hover:bg-card/80 transition-colors"
                  >
                    <div className="mb-2 flex items-start gap-2">
                      <FileText className="mt-0.5 h-4 w-4 flex-shrink-0 text-accent" />
                      <div className="flex-1">
                        <p className="text-xs font-medium text-accent">{source.metadata.source}</p>
                        <p className="text-xs text-muted-foreground">
                          Page {source.metadata.page_label} of {source.metadata.total_pages}
                        </p>
                      </div>
                    </div>
                    <p className="line-clamp-2 text-xs text-foreground/80 leading-relaxed">
                      {source.content.substring(0, 150)}...
                    </p>
                  </div>
                ))}
              </CollapsibleContent>
            </Collapsible>
          </div>
        )}
      </div>
    </div>
  )
}
