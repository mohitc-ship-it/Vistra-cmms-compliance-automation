"use client"

import type React from "react"
import { usePathname } from "next/navigation"
import { Sidebar } from "@/components/layout/sidebar"
import { Topbar } from "@/components/layout/topbar"
import { ChatbotOverlay } from "@/components/chatbot/chatbot-overlay"

export default function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname()
  return (
    <div className="min-h-dvh bg-background text-foreground">
      <div className="flex">
        <Sidebar activePath={pathname} />
        <div className="flex-1">
          <Topbar />
          <main className="p-6">{children}</main>
        </div>
      </div>
      <ChatbotOverlay />
    </div>
  )
}
