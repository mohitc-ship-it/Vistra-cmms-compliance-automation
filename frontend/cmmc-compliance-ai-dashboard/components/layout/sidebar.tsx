"use client"

import Link from "next/link"
import { useMemo } from "react"
import { cn } from "@/lib/utils"

const navItems = [
  { href: "/dashboard", label: "Dashboard" },
  { href: "/upload", label: "Upload" },
  { href: "/poam", label: "POA&M" },
  { href: "/chatbot", label: "Chatbot" },
  { href: "/audit-logs", label: "Audit Logs" },
]

export function Sidebar({ activePath }: { activePath?: string | null }) {
  const items = useMemo(() => navItems, [])
  return (
    <aside
      className="hidden md:flex w-64 shrink-0 flex-col gap-2 border-r border-sidebar-border bg-sidebar p-4"
      aria-label="Primary"
    >
      <h1 className="text-lg font-semibold text-sidebar-foreground">CMMC Compliance</h1>
      <nav className="mt-2 grid gap-1">
        {items.map((it) => {
          const active = activePath?.startsWith(it.href)
          return (
            <Link
              key={it.href}
              href={it.href}
              className={cn(
                "rounded-md px-3 py-2 text-sm outline-none transition-colors",
                active
                  ? "bg-sidebar-primary text-sidebar-primary-foreground"
                  : "text-sidebar-foreground hover:bg-sidebar-accent hover:text-sidebar-accent-foreground",
              )}
            >
              {it.label}
            </Link>
          )
        })}
      </nav>
      <div className="mt-auto rounded-md border border-sidebar-border p-3 text-xs text-sidebar-foreground/80">
        <p className="font-medium">Tip</p>
        <p>Upload SSP or policy docs to auto-map to controls.</p>
      </div>
    </aside>
  )
}
