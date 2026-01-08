// // "use client"

// // import { useState } from "react"
// // import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
// // import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
// // import { Button } from "@/components/ui/button"
// // import { Dialog, DialogContent, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
// // import { Input } from "@/components/ui/input"
// // import { Progress } from "@/components/ui/progress"

// // type Row = {
// //   id: string
// //   action: string
// //   owner: string
// //   targetDate: string
// //   progress: number
// // }

// // const initialRows: Row[] = [
// //   {
// //     id: "IA.L2-3.5.3",
// //     action: "Implement MFA for VPN and admin accounts",
// //     owner: "Alex",
// //     targetDate: "2025-11-30",
// //     progress: 30,
// //   },
// //   { id: "AC.L1-3.1.2", action: "Harden workstation baseline", owner: "Jamie", targetDate: "2025-12-15", progress: 50 },
// // ]

// // export function PoamTable() {
// //   const [rows, setRows] = useState<Row[]>(initialRows)
// //   const [editing, setEditing] = useState<Row | null>(null)

// //   const updateRow = (next: Row) => {
// //     setRows((prev) => prev.map((r) => (r.id === next.id ? next : r)))
// //     setEditing(null)
// //   }

// //   return (
// //     <Card>
// //       <CardHeader>
// //         <CardTitle className="text-sm">POA&amp;M Tracker</CardTitle>
// //       </CardHeader>
// //       <CardContent>
// //         <Table>
// //           <TableHeader>
// //             <TableRow>
// //               <TableHead>Control ID</TableHead>
// //               <TableHead>Action Item</TableHead>
// //               <TableHead>Owner</TableHead>
// //               <TableHead>Target Date</TableHead>
// //               <TableHead>Progress</TableHead>
// //               <TableHead className="text-right">Edit</TableHead>
// //             </TableRow>
// //           </TableHeader>
// //           <TableBody>
// //             {rows.map((r) => (
// //               <TableRow key={r.id}>
// //                 <TableCell className="font-mono text-sm">{r.id}</TableCell>
// //                 <TableCell className="text-sm">{r.action}</TableCell>
// //                 <TableCell>{r.owner}</TableCell>
// //                 <TableCell>{r.targetDate}</TableCell>
// //                 <TableCell className="w-40">
// //                   <div className="flex items-center gap-2">
// //                     <Progress value={r.progress} className="h-2" />
// //                     <span className="text-xs">{r.progress}%</span>
// //                   </div>
// //                 </TableCell>
// //                 <TableCell className="text-right">
// //                   <Dialog>
// //                     <DialogTrigger asChild>
// //                       <Button size="sm" variant="secondary" onClick={() => setEditing(r)}>
// //                         Edit
// //                       </Button>
// //                     </DialogTrigger>
// //                     {editing?.id === r.id && (
// //                       <EditDialog row={editing} onSave={updateRow} onClose={() => setEditing(null)} />
// //                     )}
// //                   </Dialog>
// //                 </TableCell>
// //               </TableRow>
// //             ))}
// //           </TableBody>
// //         </Table>
// //       </CardContent>
// //     </Card>
// //   )
// // }

// // function EditDialog({ row, onSave, onClose }: { row: Row; onSave: (r: Row) => void; onClose: () => void }) {
// //   const [draft, setDraft] = useState<Row>(row)
// //   return (
// //     <DialogContent>
// //       <DialogHeader>
// //         <DialogTitle>Edit {row.id}</DialogTitle>
// //       </DialogHeader>
// //       <div className="grid gap-3">
// //         <label className="grid gap-1 text-sm">
// //           <span>Action Item</span>
// //           <Input value={draft.action} onChange={(e) => setDraft({ ...draft, action: e.target.value })} />
// //         </label>
// //         <label className="grid gap-1 text-sm">
// //           <span>Owner</span>
// //           <Input value={draft.owner} onChange={(e) => setDraft({ ...draft, owner: e.target.value })} />
// //         </label>
// //         <label className="grid gap-1 text-sm">
// //           <span>Target Date</span>
// //           <Input
// //             type="date"
// //             value={draft.targetDate}
// //             onChange={(e) => setDraft({ ...draft, targetDate: e.target.value })}
// //           />
// //         </label>
// //         <label className="grid gap-1 text-sm">
// //           <span>Progress %</span>
// //           <Input
// //             type="number"
// //             min={0}
// //             max={100}
// //             value={draft.progress}
// //             onChange={(e) => setDraft({ ...draft, progress: Number(e.target.value) })}
// //           />
// //         </label>
// //       </div>
// //       <DialogFooter>
// //         <Button variant="ghost" onClick={onClose}>
// //           Cancel
// //         </Button>
// //         <Button onClick={() => onSave(draft)}>Save</Button>
// //       </DialogFooter>
// //     </DialogContent>
// //   )
// // }

// "use client"

// import { useState, useMemo } from "react"
// import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
// import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
// import { Button } from "@/components/ui/button"
// import { Dialog, DialogContent, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
// import { Input } from "@/components/ui/input"
// import { Progress } from "@/components/ui/progress"

// type Row = {
//   id: string
//   weakness: string
//   mitigation: string
//   owner: string
//   level: string
//   targetDate: string
//   progress: number
// }

// type PoamTableProps = {
//   levelFilter?: string
// }

// const initialRows: Row[] = [
//   {
//     id: "IA.L2-3.5.3",
//     weakness: "VPN and admin accounts not protected with MFA",
//     mitigation: "Implement MFA for VPN and admin accounts",
//     owner: "Alex",
//     level: "Level 2",
//     targetDate: "2025-11-30",
//     progress: 30,
//   },
//   {
//     id: "AC.L1-3.1.2",
//     weakness: "Workstation baseline not fully hardened",
//     mitigation: "Harden workstation baseline",
//     owner: "Jamie",
//     level: "Level 1",
//     targetDate: "2025-12-15",
//     progress: 50,
//   },
// ]

// export function PoamTable({ levelFilter = "All" }: PoamTableProps) {
//   const [rows, setRows] = useState<Row[]>(initialRows)
//   const [editing, setEditing] = useState<Row | null>(null)

//   const filteredRows = useMemo(() => {
//     if (levelFilter === "All") return rows
//     return rows.filter((r) => r.level === levelFilter)
//   }, [rows, levelFilter])

//   const updateRow = (next: Row) => {
//     setRows((prev) => prev.map((r) => (r.id === next.id ? next : r)))
//     setEditing(null)
//   }

//   return (
//     <Card>
//       <CardHeader>
//         <CardTitle className="text-sm">POA&amp;M Tracker</CardTitle>
//       </CardHeader>
//       <CardContent>
//         <Table>
//           <TableHeader>
//             <TableRow>
//               <TableHead className="whitespace-normal">Control ID</TableHead>
//               <TableHead className="whitespace-normal">Weakness</TableHead>
//               <TableHead className="whitespace-normal">Mitigation</TableHead>
//               <TableHead className="whitespace-normal">Owner</TableHead>
//               <TableHead className="whitespace-normal">Level</TableHead>
//               <TableHead className="whitespace-normal">Target Date</TableHead>
//               <TableHead className="whitespace-normal">Progress</TableHead>
//               <TableHead className="text-right whitespace-normal">Edit</TableHead>
//             </TableRow>
//           </TableHeader>
//           <TableBody>
//             {filteredRows.map((r) => (
//               <TableRow key={r.id} className="align-top">
//                 <TableCell className="font-mono text-sm whitespace-normal break-words">{r.id}</TableCell>
//                 <TableCell className="text-sm whitespace-normal break-words">{r.weakness}</TableCell>
//                 <TableCell className="text-sm whitespace-normal break-words">{r.mitigation}</TableCell>
//                 <TableCell className="whitespace-normal">{r.owner}</TableCell>
//                 <TableCell className="whitespace-normal">{r.level}</TableCell>
//                 <TableCell className="whitespace-normal">{r.targetDate}</TableCell>
//                 <TableCell className="w-40">
//                   <div className="flex items-center gap-2">
//                     <Progress value={r.progress} className="h-2" />
//                     <span className="text-xs">{r.progress}%</span>
//                   </div>
//                 </TableCell>
//                 <TableCell className="text-right whitespace-normal">
//                   <Dialog>
//                     <DialogTrigger asChild>
//                       <Button size="sm" variant="secondary" onClick={() => setEditing(r)}>
//                         Edit
//                       </Button>
//                     </DialogTrigger>
//                     {editing?.id === r.id && (
//                       <EditDialog row={editing} onSave={updateRow} onClose={() => setEditing(null)} />
//                     )}
//                   </Dialog>
//                 </TableCell>
//               </TableRow>
//             ))}
//             {filteredRows.length === 0 && (
//               <TableRow>
//                 <TableCell colSpan={8} className="text-center text-gray-400 whitespace-normal">
//                   No POA&M items for this level.
//                 </TableCell>
//               </TableRow>
//             )}
//           </TableBody>
//         </Table>
//       </CardContent>
//     </Card>
//   )
// }

// function EditDialog({ row, onSave, onClose }: { row: Row; onSave: (r: Row) => void; onClose: () => void }) {
//   const [draft, setDraft] = useState<Row>(row)
//   return (
//     <DialogContent>
//       <DialogHeader>
//         <DialogTitle>Edit {row.id}</DialogTitle>
//       </DialogHeader>
//       <div className="grid gap-3">
//         <label className="grid gap-1 text-sm">
//           <span>Weakness</span>
//           <Input value={draft.weakness} onChange={(e) => setDraft({ ...draft, weakness: e.target.value })} />
//         </label>
//         <label className="grid gap-1 text-sm">
//           <span>Mitigation</span>
//           <Input value={draft.mitigation} onChange={(e) => setDraft({ ...draft, mitigation: e.target.value })} />
//         </label>
//         <label className="grid gap-1 text-sm">
//           <span>Owner</span>
//           <Input value={draft.owner} onChange={(e) => setDraft({ ...draft, owner: e.target.value })} />
//         </label>
//         <label className="grid gap-1 text-sm">
//           <span>Level</span>
//           <Input value={draft.level} onChange={(e) => setDraft({ ...draft, level: e.target.value })} />
//         </label>
//         <label className="grid gap-1 text-sm">
//           <span>Target Date</span>
//           <Input
//             type="date"
//             value={draft.targetDate}
//             onChange={(e) => setDraft({ ...draft, targetDate: e.target.value })}
//           />
//         </label>
//         <label className="grid gap-1 text-sm">
//           <span>Progress %</span>
//           <Input
//             type="number"
//             min={0}
//             max={100}
//             value={draft.progress}
//             onChange={(e) => setDraft({ ...draft, progress: Number(e.target.value) })}
//           />
//         </label>
//       </div>
//       <DialogFooter>
//         <Button variant="ghost" onClick={onClose}>
//           Cancel
//         </Button>
//         <Button onClick={() => onSave(draft)}>Save</Button>
//       </DialogFooter>
//     </DialogContent>
//   )
// }
"use client"

import { useState, useMemo, useEffect } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Button } from "@/components/ui/button"
import { Dialog, DialogContent, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { exportToCSV } from "@/lib/export"

type Row = {
  assessment: string
  controlId: string // CMMC ID
  weakness: string
  mitigation: string
  status: string
  owner: string
  targetDate: string
}

type PoamTableProps = {
  levelFilter?: string
}

const randomOwners = ["Alex", "Jamie", "Taylor", "Jordan", "Morgan"]
const randomDates = ["2025-11-30", "2025-12-15", "2026-01-10", "2026-02-20"]

const initialRows: Omit<Row, "owner" | "targetDate">[] = [
  {
    assessment: "CUI Enclave",
    controlId: "3.1.2",
    weakness:
      "The organization has not fully defined or standardized the types of transactions and functions that each user role is permitted to execute.",
    mitigation:
      "Define and document access permissions by role. Implement RBAC. Conduct periodic access reviews and audits.",
    status: "Completed",
  },
  {
    assessment: "CUI Enclave",
    controlId: "3.1.4",
    weakness:
      "The organization has not effectively separated critical duties, allowing individuals to bypass internal controls.",
    mitigation: "Define critical roles and responsibilities. Implement SoD controls. Regular review and monitoring.",
    status: "In-Progress",
  },
]

export default function PoamTable({ levelFilter = "All" }: PoamTableProps) {
  const [rows, setRows] = useState<Row[]>([])
  const [editing, setEditing] = useState<Row | null>(null)

  useEffect(() => {
    const populated = initialRows.map((r) => ({
      ...r,
      owner: randomOwners[Math.floor(Math.random() * randomOwners.length)],
      targetDate: randomDates[Math.floor(Math.random() * randomDates.length)],
    }))
    setRows(populated)
  }, [])

  const filteredRows = useMemo(() => {
    if (levelFilter === "All") return rows
    return rows.filter((r) => r.controlId.startsWith(levelFilter))
  }, [rows, levelFilter])

  const handleExport = () => {
    exportToCSV("poam.csv", filteredRows)
  }

  const updateRow = (next: Row) => {
    setRows((prev) => prev.map((r) => (r.controlId === next.controlId ? next : r)))
    setEditing(null)
  }

  return (
    <Card className="max-w-full md:max-w-7xl mx-auto">
      <CardHeader className="flex items-center justify-between">
        <CardTitle className="text-sm">POA&M Tracker</CardTitle>
        {/* <Button size="sm" variant="secondary" onClick={handleExport}>
          Export to CSV
        </Button> */}
      </CardHeader>
      <CardContent className="overflow-x-auto">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Assessment</TableHead>
              <TableHead>CMMC ID</TableHead>
              <TableHead>Weakness</TableHead>
              <TableHead>Mitigation</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Owner</TableHead>
              <TableHead>Target Date</TableHead>
              <TableHead className="text-right">Edit</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {filteredRows.map((r) => (
              <TableRow key={r.controlId}>
                <TableCell className="whitespace-normal break-words">{r.assessment}</TableCell>
                <TableCell className="whitespace-normal break-words">{r.controlId}</TableCell>
                <TableCell className="whitespace-normal break-words">{r.weakness}</TableCell>
                <TableCell className="whitespace-normal break-words">{r.mitigation}</TableCell>
                <TableCell className="whitespace-normal break-words">{r.status}</TableCell>
                <TableCell className="whitespace-normal break-words">{r.owner}</TableCell>
                <TableCell className="whitespace-normal break-words">{r.targetDate}</TableCell>
                <TableCell className="text-right whitespace-normal">
                  <Dialog>
                    <DialogTrigger asChild>
                      <Button size="sm" variant="secondary" onClick={() => setEditing(r)}>
                        Edit
                      </Button>
                    </DialogTrigger>
                    {editing?.controlId === r.controlId && (
                      <EditDialog row={editing} onSave={updateRow} onClose={() => setEditing(null)} />
                    )}
                  </Dialog>
                </TableCell>
              </TableRow>
            ))}
            {filteredRows.length === 0 && (
              <TableRow>
                <TableCell colSpan={8} className="text-center text-gray-400 whitespace-normal">
                  No POA&M items found.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  )
}

function EditDialog({ row, onSave, onClose }: { row: Row; onSave: (r: Row) => void; onClose: () => void }) {
  const [draft, setDraft] = useState<Row>(row)
  return (
    <DialogContent>
      <DialogHeader>
        <DialogTitle>Edit {row.controlId}</DialogTitle>
      </DialogHeader>
      <div className="grid gap-3">
        <label className="grid gap-1 text-sm">
          <span>Weakness</span>
          <Input value={draft.weakness} onChange={(e) => setDraft({ ...draft, weakness: e.target.value })} />
        </label>
        <label className="grid gap-1 text-sm">
          <span>Mitigation</span>
          <Input value={draft.mitigation} onChange={(e) => setDraft({ ...draft, mitigation: e.target.value })} />
        </label>
        <label className="grid gap-1 text-sm">
          <span>Status</span>
          <Input value={draft.status} onChange={(e) => setDraft({ ...draft, status: e.target.value })} />
        </label>
        <label className="grid gap-1 text-sm">
          <span>Owner</span>
          <Input value={draft.owner} onChange={(e) => setDraft({ ...draft, owner: e.target.value })} />
        </label>
        <label className="grid gap-1 text-sm">
          <span>Target Date</span>
          <Input
            type="date"
            value={draft.targetDate}
            onChange={(e) => setDraft({ ...draft, targetDate: e.target.value })}
          />
        </label>
      </div>
      <DialogFooter>
        <Button variant="ghost" onClick={onClose}>
          Cancel
        </Button>
        <Button onClick={() => onSave(draft)}>Save</Button>
      </DialogFooter>
    </DialogContent>
  )
}
