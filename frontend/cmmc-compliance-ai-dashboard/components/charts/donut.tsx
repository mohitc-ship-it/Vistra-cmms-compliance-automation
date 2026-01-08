"use client"

import { ResponsiveContainer, PieChart, Pie, Cell, Tooltip, PieLabelRenderProps } from "recharts"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { useMemo } from "react"

type DonutProps = {
  met: number
  notMet: number
  inProgress?: number
  title?: string
}

type DonutData = {
  name: string
  value: number
}

export function Donut({
  met,
  notMet,
  inProgress = 0,
  title = "Compliance Status",
}: DonutProps) {
  // Color palette for slices
  const COLORS = ["#22c55e", "#ef4444", "#facc15"] // green, red, yellow

  // Prepare data
  const data: DonutData[] = useMemo(
    () => [
      { name: "Met", value: met },
      { name: "Not Met", value: notMet },
      // { name: "inProgress", value: inProgress },
    ],
    [met, notMet, inProgress]
  )

  // Label renderer with proper typing
  const renderLabel = ({ name, percent }: PieLabelRenderProps) => {
    const p:any = percent ?? 0 // percent can be undefined
    return `${name} ${(p * 100).toFixed(0)}%`
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-sm">{title}</CardTitle>
      </CardHeader>
      <CardContent className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Tooltip
              contentStyle={{
                background: "#1f2937",
                border: "1px solid #374151",
                color: "#f9fafb",
              }}
            />
            <Pie
              data={data}
              dataKey="value"
              nameKey="name"
              innerRadius={60}
              outerRadius={90}
              paddingAngle={4}
              label={renderLabel}
            >
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
          </PieChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  )
}
