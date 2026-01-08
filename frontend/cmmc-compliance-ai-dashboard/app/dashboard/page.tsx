
"use client"

import { useEffect, useState } from "react"
import AppShell from "@/components/app-shell"
import { KpiCards, KPI } from "@/components/kpi/kpi-cards"
import { Donut } from "@/components/charts/donut"
import { ControlsTable } from "@/components/tables/controls-table"
import { motion } from "framer-motion"
import { Button } from "@/components/ui/button"

// Dashboard control type
export type Control = {
  id: string
  assessmentObjective: string
  framework: string
  family: string
  level: string
  sprs?: number
  status: "Met" | "Not Met" | "In-Progress" | "Not Applicable"
  [key: string]: any
}

// POA&M item type
type PoamItem = { label: string; value: number }

export default function DashboardPage() {
  const levels = ["All", "Level 1", "Level 2", "Level 3"]
  const [selectedLevel, setSelectedLevel] = useState("All")
  const [controls, setControls] = useState<Control[]>([])
  const [kpis, setKpis] = useState<KPI[]>([])
  const [loading, setLoading] = useState(false)

  const fetchDashboardData = async (level: string) => {
    setLoading(true)
    try {
      const res = await fetch(`http://localhost:8000/api/dashboard?level=${level}`)
      const data = await res.json()

      // Map backend fields to frontend Control type
      const matchedControls: Control[] = (data?.matched_rows || []).map((c: any) => {
        let normalizedStatus: "Met" | "Not Met" | "In-Progress" | "Not Applicable" = "In-Progress"
        const status = (c["Assessment Status"] ?? "").toLowerCase()
        if (status === "met") normalizedStatus = "Met"
        else if (status === "not met") normalizedStatus = "Not Met"
        else normalizedStatus = "In-Progress"

        return {
          id: c["Sort-As"] ?? "",
          assessmentObjective: c["Assessment Objective"] ?? "",
          level: c["Level"] ?? "Unknown",
          status: normalizedStatus,
          family: c["Family"] ?? "",
          framework: c["Framework"] ?? "",
          sprs: c["SPRS"] ?? 0,
        }
      })

      setControls(matchedControls)

      // Compute counts
      const total = matchedControls.length
      const met = matchedControls.filter((c) => c.status === "Met").length
      const notMet = matchedControls.filter((c) => c.status === "Not Met").length
      const inProgress = matchedControls.filter((c) => c.status === "In-Progress").length

      // Prepare KPI cards
      const dashboardMetrics: KPI[] = [
        { label: "Total Controls", value: total },
        { label: "Controls Met", value: met },
      ]

      if (data?.dashboard_metrics) {
        data.dashboard_metrics.forEach((metric: any) => {
          if (metric.label === "POA&M Progress" && Array.isArray(metric.value)) {
            const filtered: PoamItem[] = metric.value.filter(
              (v: PoamItem) => v.label !== "Not Assigned" && v.value > 0
            )
            dashboardMetrics.push({ label: metric.label, value: filtered })
          } else if (metric.label === "SPRS Score") {
            dashboardMetrics.push({ label: metric.label, value: metric.value })
          }
        })
      }

      setKpis(dashboardMetrics)
    } catch (err) {
      console.error("Failed to fetch dashboard data:", err)
      setControls([])
      setKpis([])
    }
    setLoading(false)
  }

  useEffect(() => {
    fetchDashboardData(selectedLevel)
  }, [selectedLevel])

  // Compute Donut values from controls directly
  const total = controls.length
  const met = controls.filter((c) => c.status === "Met").length
  const notMet = controls.filter((c) => c.status === "Not Met").length
  const inProgress = controls.filter((c) => c.status === "In-Progress").length
  const notApplicable = controls.filter((c) => c.status === "Not Applicable").length
  console.log("in progress lenght ", inProgress)
  console.log(notApplicable)

  // Excel download
  const downloadExcel = async () => {
    try {
      const res = await fetch("http://localhost:8000/api/download-dashboard")
      if (!res.ok) throw new Error("Failed to fetch Excel file")

      const blob = await res.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement("a")
      a.href = url
      a.download = "merged_poam_assessment.xlsx"
      document.body.appendChild(a)
      a.click()
      a.remove()
      window.URL.revokeObjectURL(url)
    } catch (err) {
      console.error("Download failed:", err)
      alert("Failed to download Excel file")
    }
  }

  return (
    <AppShell>
      <div className="grid gap-6">
        {/* Level Selector + Download */}
        <div className="flex justify-between items-center">
          <select
            className="border rounded px-3 py-1"
            value={selectedLevel}
            onChange={(e) => setSelectedLevel(e.target.value)}
          >
            {levels.map((level) => (
              <option key={level} value={level}>
                {level}
              </option>
            ))}
          </select>

          <Button size="sm" variant="secondary" onClick={downloadExcel}>
            Download Full Excel
          </Button>
        </div>

        {/* KPI Cards */}
        <KpiCards items={kpis} />

        {/* Donut + Controls Table */}
        {loading ? (
          <div>Loading dashboard data...</div>
        ) : (
          <motion.div initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }}>
            <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
              <div className="lg:col-span-1">
                <Donut met={met} notMet={notMet} inProgress={inProgress} />
              </div>
              <div className="lg:col-span-2">
                <ControlsTable data={controls} />
              </div>
            </div>
          </motion.div>
        )}
      </div>
    </AppShell>
  )
}
