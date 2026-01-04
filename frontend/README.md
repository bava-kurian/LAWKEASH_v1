# LAWkeash Frontend

The frontend for the LAWkeash Bot, built with **Next.js 14**, **Tailwind CSS**, and **React**.

## 🚀 Getting Started

### Prerequisites
-   Node.js 18+ installed.

### Installation

```bash
cd frontend
npm install
```

### Running Locally

```bash
npm run dev
```
The application will be available at `http://localhost:3000`.

## 📂 Project Structure

-   `app/`: Next.js App Router directories.
    -   `page.tsx`: Main chat page.
    -   `api/`: Backend proxy routes (`/api/v1/ask`).
-   `components/`: Reusable UI components.
    -   `chat-interface.tsx`: Main chat window logic.
    -   `chat-message.tsx`: Individual message bubbles with markdown and citation support.
    -   `ui/`: Shadcn UI components.

## 🎨 Features
-   **Markdown Support**: Bold, italic, lists, and links rendering.
-   **Dynamic Theming**: Dark/Light mode support.
-   **Responsive Design**: Mobile-friendly interface.
-   **Proxy API**: Next.js API route bridges the frontend to the FastAPI backend.
