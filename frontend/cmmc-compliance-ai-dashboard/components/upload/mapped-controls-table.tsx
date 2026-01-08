// "use client"

// import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
// import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"

// const mapped = [
//   { id: "AC.L1-3.1.1", confidence: 0.92, summary: "Access limited to authorized users." },
//   { id: "AC.L1-3.1.2", confidence: 0.81, summary: "Device use limited to authorized users." },
//   { id: "IA.L2-3.5.3", confidence: 0.74, summary: "MFA required for network access." },
// ]

// export function MappedControlsTable() {
//   return (
//     <Card>
//       <CardHeader>
//         <CardTitle className="text-sm">AI-mapped Controls</CardTitle>
//       </CardHeader>
//       <CardContent>
//         <Table>
//           <TableHeader>
//             <TableRow>
//               <TableHead>Control ID</TableHead>
//               <TableHead>Confidence %</TableHead>
//               <TableHead>Summary</TableHead>
//             </TableRow>
//           </TableHeader>
//           <TableBody>
//             {mapped.map((m) => (
//               <TableRow key={m.id}>
//                 <TableCell className="font-mono text-sm">{m.id}</TableCell>
//                 <TableCell>{Math.round(m.confidence * 100)}%</TableCell>
//                 <TableCell className="text-sm">{m.summary}</TableCell>
//               </TableRow>
//             ))}
//           </TableBody>
//         </Table>
//       </CardContent>
//     </Card>
//   )
// }

// "use client"

// import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
// import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"

// export type MappedControl = {
//   id: string
//   confidence: number
//   summary: string
// }

// type MappedControlsTableProps = {
//   data?: MappedControl[]
// }

// const DEFAULT_MAPPED: MappedControl[] = [
//   { id: "AC.L1-3.1.1", confidence: 0.92, summary: "Access limited to authorized users." },
//   { id: "AC.L1-3.1.2", confidence: 0.81, summary: "Device use limited to authorized users." },
//   { id: "IA.L2-3.5.3", confidence: 0.74, summary: "MFA required for network access." },
// ]

// export function MappedControlsTable({ data }: MappedControlsTableProps) {
//   const mappedData = data && data.length > 0 ? data : DEFAULT_MAPPED

//   return (
//     <Card>
//       <CardHeader>
//         <CardTitle className="text-sm">AI-mapped Controls</CardTitle>
//       </CardHeader>
//       <CardContent>
//         <Table>
//           <TableHeader>
//             <TableRow>
//               <TableHead>Control ID</TableHead>
//               <TableHead>Confidence %</TableHead>
//               <TableHead>Summary</TableHead>
//             </TableRow>
//           </TableHeader>
//           <TableBody>
//             {mappedData.map((m) => (
//               <TableRow key={m.id}>
//                 <TableCell className="font-mono text-sm">{m.id}</TableCell>
//                 <TableCell>{Math.round(m.confidence * 100)}%</TableCell>
//                 <TableCell className="text-sm">{m.summary}</TableCell>
//               </TableRow>
//             ))}
//           </TableBody>
//         </Table>
//       </CardContent>
//     </Card>
//   )
// }

// "use client"

// import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
// import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"

// export type MappedControl = {
//   id: string
//   confidence: number
//   summary: string
// }

// type MappedControlsTableProps = {
//   data: MappedControl[]
// }

// export function MappedControlsTable({ data }: MappedControlsTableProps) {
//   if (!data || data.length === 0) return null // hide table if no data

//   return (
//     <Card>
//       <CardHeader>
//         <CardTitle className="text-sm">AI-mapped Controls</CardTitle>
//       </CardHeader>
//       <CardContent>
//         <Table>
//           <TableHeader>
//             <TableRow>
//               <TableHead>Control ID</TableHead>
//               <TableHead>Confidence %</TableHead>
//               <TableHead>Summary</TableHead>
//             </TableRow>
//           </TableHeader>
//           <TableBody>
//             {data.map((m) => (
//               <TableRow key={m.id}>
//                 <TableCell className="font-mono text-sm">{m.id}</TableCell>
//                 <TableCell>{Math.round(m.confidence * 100)}%</TableCell>
//                 <TableCell className="text-sm">{m.summary}</TableCell>
//               </TableRow>
//             ))}
//           </TableBody>
//         </Table>
//       </CardContent>
//     </Card>
//   )
// }

"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"

export type MappedControl = {
  id: string
  confidence: number
  summary: string
}

type MappedControlsTableProps = {
  data: MappedControl[]
}

export function MappedControlsTable({ data }: MappedControlsTableProps) {
  if (!data || data.length === 0) return null

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-sm">AI-mapped Controls</CardTitle>
      </CardHeader>
      <CardContent>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Control ID</TableHead>
              <TableHead>Confidence %</TableHead>
              <TableHead>Summary</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {data.map((m) => (
              <TableRow key={m.id}>
                <TableCell className="font-mono text-sm">{m.id}</TableCell>
                <TableCell>{Math.round(m.confidence * 100)}%</TableCell>
                <TableCell className="text-sm">{m.summary}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  )
}
