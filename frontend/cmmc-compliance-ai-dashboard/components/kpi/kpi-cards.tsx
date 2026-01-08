// "use client"

// import React from "react"

// export type KPI = {
//   label: string
//   value: string | number
// }

// type KpiCardsProps = {
//   items: KPI[]
// }

// export function KpiCards({ items }: KpiCardsProps) {
//   return (
//     <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
//       {items.map((kpi) => (
//         <div
//           key={kpi.label}
//           className="p-4 rounded-2xl shadow-md flex flex-col justify-center hover:shadow-lg transition-shadow"
//         >
//           <div className="text-sm text-gray-500">{kpi.label}</div>
//           <div className="mt-2 text-2xl font-semibold text-gray-900">{kpi.value}</div>
//         </div>
//       ))}
//     </div>
//   )
// }

"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { motion } from "framer-motion"

type KPIValue = number | string | { label: string; value: number }[]

export type KPI = {
  label: string
  value: KPIValue
  sub?: string
}

export function KpiCards({ items }: { items: KPI[] }) {
  return (
    <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-4">
      {items.map((kpi, i) => (
        <motion.div
          key={kpi.label}
          initial={{ opacity: 0, y: 6 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.05 * i }}
        >
          <Card className="rounded-2xl shadow-md p-4 bg-gray-800 text-white">
            <CardHeader className="flex flex-col">
              <CardTitle className="text-sm text-gray-300">{kpi.label}</CardTitle>

              {/* Single value */}
              {typeof kpi.value === "number" || typeof kpi.value === "string" ? (
                <div className="mt-2 text-2xl font-bold">{kpi.value}</div>
              ) : Array.isArray(kpi.value) ? (
                <div className="mt-2 flex flex-col space-y-1">
                  {(kpi.value as { label: string; value: number }[]).map((v) => (
                    <Badge
                      key={v.label}
                      variant={v.value > 0 ? "default" : "secondary"}
                      className="text-sm text-white"
                    >
                      {v.label}: {v.value}
                    </Badge>
                  ))}
                </div>
              ) : null}
            </CardHeader>
          </Card>
        </motion.div>
      ))}
    </div>
  )
}
