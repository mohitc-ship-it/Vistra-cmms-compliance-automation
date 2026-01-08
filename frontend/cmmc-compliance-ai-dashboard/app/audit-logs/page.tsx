"use client"

import AppShell from "@/components/app-shell"
import { AuditLogTable } from "@/components/tables/audit-log-table"
import { motion } from "framer-motion"

export default function AuditLogsPage() {
  return (
    <AppShell>
      <motion.div initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }}>
        <AuditLogTable />
      </motion.div>
    </AppShell>
  )
}
