"use client"

import AppShell from "@/components/app-shell"
import { UploadPanel } from "@/components/upload/upload-panel"
import { motion } from "framer-motion"

export default function UploadPage() {
  return (
    <AppShell>
      <motion.div initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }}>
        <UploadPanel />
      </motion.div>
    </AppShell>
  )
}
