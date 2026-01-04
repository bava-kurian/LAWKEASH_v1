"use client"

import type React from "react"

import { useState, useRef, useEffect } from "react"
import { MessageCircle, Send, AlertCircle } from "lucide-react"
import ChatMessage from "./chat-message"
import { ThemeToggle } from "./theme-toggle"
import { LoadingSpinner } from "./loading-spinner"

interface Message {
  id: string
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

export default function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim()) return

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: input,
    }

    setMessages((prev) => [...prev, userMessage])
    setInput("")
    setIsLoading(true)

    try {
      const response = await fetch("/api/v1/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: input }),
      })

      if (!response.ok) throw new Error("Failed to get response")

      const data = await response.json()

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: data.answer,
        sources: data.sources,
      }

      setMessages((prev) => [...prev, assistantMessage])
    } catch (error) {
      console.error("Error:", error)
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: "An error occurred while processing your question. Please try again.",
      }
      setMessages((prev) => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="flex h-screen w-full flex-col bg-background transition-colors duration-300">
      <div className="border-b border-border/50 bg-card/50 backdrop-blur-md transition-colors duration-300">
        <div className="flex items-center justify-between px-6 py-4">
          <div className="flex items-center gap-3">
            <div className="rounded-lg bg-gradient-to-br from-primary to-accent p-2 transition-colors duration-300">
              <MessageCircle className="h-6 w-6 text-primary-foreground" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-foreground transition-colors duration-300">LAWkeash BOT</h1>
              <p className="text-sm text-muted-foreground transition-colors duration-300">Indian Law AI Assistant</p>
            </div>
          </div>
          <ThemeToggle />
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 overflow-y-auto transition-colors duration-300">
        {messages.length === 0 ? (
          <div className="flex h-full flex-col items-center justify-center px-4 py-12">
            <div className="mb-8 rounded-2xl bg-gradient-to-br from-primary/20 via-accent/10 to-secondary/20 p-8 transition-colors duration-300">
              <MessageCircle className="h-16 w-16 text-accent transition-colors duration-300" />
            </div>
            <h2 className="mb-2 text-center text-2xl font-bold text-foreground transition-colors duration-300">
              Welcome to LAWkeash BOT
            </h2>
            <p className="mb-8 max-w-md text-center text-muted-foreground transition-colors duration-300">
              Your AI-powered assistant for Indian Law. Ask questions to get instant legal insights powered by
              retrieval-augmented generation.
            </p>
            <div className="grid gap-3 sm:grid-cols-2">
              <div className="rounded-lg border border-border bg-card/50 p-4 text-center transition-colors duration-300">
                <MessageCircle className="mx-auto mb-2 h-5 w-5 text-primary transition-colors duration-300" />
                <p className="text-sm font-medium text-foreground transition-colors duration-300">Ask Questions</p>
              </div>
              <div className="rounded-lg border border-border bg-card/50 p-4 text-center transition-colors duration-300">
                <AlertCircle className="mx-auto mb-2 h-5 w-5 text-destructive transition-colors duration-300" />
                <p className="text-sm font-medium text-foreground transition-colors duration-300">Get Citations</p>
              </div>
            </div>
          </div>
        ) : (
          <div className="space-y-4 p-6">
            {messages.map((message) => (
              <ChatMessage key={message.id} message={message} />
            ))}
            {isLoading && (
              <div className="flex justify-start animate-slide-in">
                <div className="rounded-lg bg-card border border-border/50 px-4 py-3">
                  <LoadingSpinner />
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      {/* Input Area */}
      <div className="border-t border-border/50 bg-card/50 backdrop-blur-md px-6 py-4 transition-colors duration-300">
        <form onSubmit={handleSendMessage} className="flex gap-3">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask a question about Indian Law..."
            disabled={isLoading}
            className="flex-1 rounded-lg border border-border bg-input px-4 py-3 text-foreground placeholder:text-muted-foreground focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/50 disabled:opacity-50 transition-colors duration-300"
          />
          <button
            type="submit"
            disabled={isLoading || !input.trim()}
            className="rounded-lg bg-primary px-4 py-3 text-primary-foreground transition-all hover:bg-primary/90 active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Send className="h-4 w-4" />
          </button>
        </form>
        <p className="mt-2 text-center text-xs text-muted-foreground transition-colors duration-300">
          LAWkeash BOT uses RAG technology to provide accurate legal references from uploaded documents.
        </p>
      </div>
    </div>
  )
}
