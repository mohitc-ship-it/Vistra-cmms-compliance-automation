"use client"

import { useMemo, useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Input } from "@/components/ui/input"

type Log = {
  ts: string
  action: string
  details: string
  user: string
}

const logs: Log[] = [
  { ts: "2025-10-10 09:15", action: "Upload", details: "SSP_v3.pdf uploaded", user: "alex" },
  { ts: "2025-10-10 09:16", action: "AI Map", details: "42 controls mapped", user: "alex" },
  { ts: "2025-10-10 10:05", action: "Edit POA&M", details: "IA.L2-3.5.3 progress 10%→30%", user: "jamie" },
  { ts: "2025-10-11 08:40", action: "Export", details: "Report downloaded", user: "alex" },
]

export function AuditLogTable() {
  const [user, setUser] = useState("")
  const [date, setDate] = useState("")

  const filtered = useMemo(() => {
    return logs.filter((l) => {
      const okUser = user ? l.user.includes(user) : true
      const okDate = date ? l.ts.startsWith(date) : true
      return okUser && okDate
    })
  }, [user, date])

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-sm">Audit Log</CardTitle>
      </CardHeader>
      <CardContent className="grid gap-3">
        <div className="flex flex-wrap items-center gap-3">
          <div className="grid gap-1">
            <label className="text-xs">Filter by user</label>
            <Input placeholder="e.g. alex" value={user} onChange={(e) => setUser(e.target.value)} />
          </div>
          <div className="grid gap-1">
            <label className="text-xs">Filter by date</label>
            <Input type="date" value={date} onChange={(e) => setDate(e.target.value)} />
          </div>
        </div>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Timestamp</TableHead>
              <TableHead>Action</TableHead>
              <TableHead>Details</TableHead>
              <TableHead>User</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {filtered.map((l, i) => (
              <TableRow key={i}>
                <TableCell className="whitespace-nowrap">{l.ts}</TableCell>
                <TableCell>{l.action}</TableCell>
                <TableCell className="text-sm">{l.details}</TableCell>
                <TableCell className="font-medium">{l.user}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  )
}
