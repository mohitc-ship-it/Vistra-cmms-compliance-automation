"use client"

import { Button } from "@/components/ui/button"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { exportToCSV } from "@/lib/export"
import { useCallback } from "react"

export function Topbar() {
  const onExport = useCallback(() => {
    // Dummy report data
    exportToCSV("cmmc-report.csv", [
      { metric: "Total Controls", value: 110 },
      { metric: "Controls Met", value: 72 },
      { metric: "SPRS Score", value: 78 },
      { metric: "POA&M Progress (%)", value: 42 },
    ])
  }, [])

  return (
    <header className="sticky top-0 z-10 flex items-center justify-between border-b bg-card/70 p-4 backdrop-blur">
      <div className="flex items-center gap-3">
        <div className="h-2 w-2 rounded-full bg-primary" aria-hidden />
        <span className="text-sm font-semibold text-pretty">CMMC Compliance AI Dashboard</span>
      </div>
      <div className="flex items-center gap-3">
        <Button variant="default" onClick={onExport}>
          Export Report
        </Button>
        <Avatar>
          <AvatarFallback>JD</AvatarFallback>
        </Avatar>
      </div>
    </header>
  )
}
