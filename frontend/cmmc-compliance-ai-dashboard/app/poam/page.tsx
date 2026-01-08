// "use client"

// import AppShell from "@/components/app-shell"
// import { PoamTable } from "@/components/tables/poam-table"
// import { motion } from "framer-motion"

// export default function PoamPage() {
//   return (
//     <AppShell>
//       <motion.div initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }}>
//         <PoamTable />
//       </motion.div>
//     </AppShell>
//   )
// }


"use client"

import { useState } from "react"
import AppShell from "@/components/app-shell"
import PoamTable  from "@/components/tables/poam-table"
import { motion } from "framer-motion"

export default function PoamPage() {
  const levels = ["All", "Level 1", "Level 2", "Level 3"]
  const [selectedLevel, setSelectedLevel] = useState("All")

  return (
    <AppShell>
      <div className="mb-4 flex justify-end">
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
      </div>
      <motion.div initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }}>
        <PoamTable levelFilter={selectedLevel} />
      </motion.div>
    </AppShell>
  )
}
