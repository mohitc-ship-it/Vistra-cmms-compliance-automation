"use client"

import { useState, useMemo } from "react"
import { Badge } from "@/components/ui/badge"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Button } from "@/components/ui/button"

type ControlsTableProps = {
  data?: Record<string, any>[] // dynamic column support
}

export function ControlsTable({ data }: ControlsTableProps) {
  const [levelFilter, setLevelFilter] = useState<string>("All")
  const [statusFilter, setStatusFilter] = useState<string>("All")
  const [showFramework, setShowFramework] = useState<boolean>(true) // Toggle for framework/nist_id column

  // Apply filters
  const filteredControls = useMemo(() => {
    if (!data) return []
    return data
      .filter((c) => levelFilter === "All" || c.level === levelFilter)
      .filter((c) => statusFilter === "All" || c.status === statusFilter)
  }, [data, levelFilter, statusFilter])

  // Unique values for dropdowns
  const levels = useMemo(
    () => Array.from(new Set(data?.map((c) => c.level).filter(Boolean) ?? [])),
    [data]
  )
  const statuses = ["Met", "Not Met", "In-Progress"]

  // Download Excel
  const downloadExcel = async () => {
    try {
      const res = await fetch(`http://localhost:8000/api/download-dashboard`)
      if (!res.ok) throw new Error("Failed to fetch Excel file")
      const blob = await res.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement("a")
      a.href = url
      a.download = `merged_poam_assessment.xlsx`
      document.body.appendChild(a)
      a.click()
      a.remove()
      window.URL.revokeObjectURL(url)
    } catch (err) {
      console.error("Download failed:", err)
      alert("Failed to download Excel file")
    }
  }

  // Table columns
  const columns = useMemo(() => {
    if (!data || data.length === 0) return []
    const keys = new Set<string>()
    data.forEach((row) => Object.keys(row).forEach((k) => keys.add(k)))
    let cols = Array.from(keys)
    if (!showFramework) {
      cols = cols.filter((c) => c !== "framework" && c !== "nist_id")
    }
    return cols
  }, [data, showFramework])

  return (
    <Card className="mt-6">
      <CardHeader className="flex flex-row items-center justify-between">
        <CardTitle className="text-sm">Controls</CardTitle>
        <Button size="sm" variant="secondary" onClick={downloadExcel}>
          Export to Excel
        </Button>
      </CardHeader>
      <CardContent>
        {/* Filters */}
        <div className="flex gap-4 mb-4 flex-wrap items-center">
          <div>
            <label className="text-sm mr-2">Level:</label>
            <select
              className="border rounded px-2 py-1 text-sm"
              value={levelFilter}
              onChange={(e) => setLevelFilter(e.target.value)}
            >
              <option value="All">All</option>
              {levels.map((lvl, idx) => (
                <option key={`${lvl}-${idx}`} value={lvl}>
                  {lvl}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="text-sm mr-2">Status:</label>
            <select
              className="border rounded px-2 py-1 text-sm"
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
            >
              <option value="All">All</option>
              {statuses.map((s, idx) => (
                <option key={`${s}-${idx}`} value={s}>
                  {s}
                </option>
              ))}
            </select>
          </div>

          <div className="flex items-center gap-2">
            <input
              type="checkbox"
              id="showFramework"
              checked={showFramework}
              onChange={() => setShowFramework((prev) => !prev)}
            />
            <label htmlFor="showFramework" className="text-sm">
              Show Framework / NIST ID
            </label>
          </div>
        </div>

        {/* Table */}
        <div className="overflow-y-auto max-h-[500px] border rounded">
          <Table className="table-fixed w-full border-collapse">
            <TableHeader>
              <TableRow>
                {columns.map((col) => (
                  <TableHead key={col} className="text-left">
                    {col}
                  </TableHead>
                ))}
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredControls.map((row, idx) => (
                <TableRow key={idx} className="align-top">
                  {columns.map((col) => (
                    <TableCell key={col} className="text-sm break-words whitespace-normal">
                      {col === "status" ? (
                        <Badge
                          variant={
                            row[col] === "Met"
                              ? "default"
                              : row[col] === "Not Met"
                              ? "destructive"
                              : "secondary"
                          }
                        >
                          {row[col]}
                        </Badge>
                      ) : (
                        row[col] ?? "-"
                      )}
                    </TableCell>
                  ))}
                </TableRow>
              ))}
              {filteredControls.length === 0 && (
                <TableRow>
                  <TableCell colSpan={columns.length} className="text-center text-gray-400">
                    No controls found for this filter.
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </div>
      </CardContent>
    </Card>
  )
}
