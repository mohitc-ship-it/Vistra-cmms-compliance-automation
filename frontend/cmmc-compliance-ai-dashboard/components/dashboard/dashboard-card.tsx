"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

type DashboardCardProps = {
  label: string
  value: string | number
  sub?: string
}

export function DashboardCard({ label, value, sub }: DashboardCardProps) {
  return (
    <Card className="rounded-lg border bg-card">
      <CardHeader>
        <CardTitle className="text-sm text-muted-foreground">{label}</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-semibold">{value}</div>
        {sub ? <div className="text-xs text-muted-foreground">{sub}</div> : null}
      </CardContent>
    </Card>
  )
}
