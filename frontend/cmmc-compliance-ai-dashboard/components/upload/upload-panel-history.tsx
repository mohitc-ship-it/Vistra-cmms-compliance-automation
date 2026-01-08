// "use client"

// import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
// import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
// import { MappedControl, MappedControlsTable } from "./mapped-controls-table"

// export type UploadedHistory = {
//   name: string
//   size: number
//   type: string
//   mappedControls?: MappedControl[]
// }

// type UploadHistoryPanelProps = {
//   history: UploadedHistory[]
// }

// export function UploadHistoryPanel({ history }: UploadHistoryPanelProps) {
//   if (!history || history.length === 0) return null

//   return (
//     <Card>
//       <CardHeader>
//         <CardTitle className="text-sm">Uploaded Files History</CardTitle>
//       </CardHeader>
//       <CardContent className="grid gap-4">
//         {/* Files table */}
//         <div className="rounded-lg border">
//           <Table>
//             <TableHeader>
//               <TableRow>
//                 <TableHead>File Name</TableHead>
//                 <TableHead>Type</TableHead>
//                 <TableHead className="text-right">Size (KB)</TableHead>
//               </TableRow>
//             </TableHeader>
//             <TableBody>
//               {history.map((f, i) => (
//                 <TableRow key={`${f.name}-${i}`}>
//                   <TableCell className="text-sm">{f.name}</TableCell>
//                   <TableCell className="text-xs text-muted-foreground">{f.type}</TableCell>
//                   <TableCell className="text-right text-xs">{Math.round(f.size / 1024)}</TableCell>
//                 </TableRow>
//               ))}
//             </TableBody>
//           </Table>
//         </div>

//         {/* Mapped controls for each file */}
//         {history.map(
//           (f, idx) =>
//             f.mappedControls &&
//             f.mappedControls.length > 0 && (
//               <div key={`mapped-${idx}`}>
//                 <MappedControlsTable data={f.mappedControls} />
//               </div>
//             ),
//         )}
//       </CardContent>
//     </Card>
//   )
// }

"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { MappedControlsTable, MappedControl } from "./mapped-controls-table"

export type UploadedHistory = {
  name: string
  size: number
  type: string
  mappedControls?: MappedControl[]
}

type UploadHistoryPanelProps = {
  history: UploadedHistory[]
}

export function UploadHistoryPanel({ history }: UploadHistoryPanelProps) {
  if (!history || history.length === 0) return null

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-sm">Uploaded Files History</CardTitle>
      </CardHeader>
      <CardContent className="grid gap-4">
        {/* Files table */}
        <div className="rounded-lg border">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>File Name</TableHead>
                <TableHead>Type</TableHead>
                <TableHead className="text-right">Size (KB)</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {history.map((f, i) => (
                <TableRow key={`${f.name}-${i}`}>
                  <TableCell className="text-sm">{f.name}</TableCell>
                  <TableCell className="text-xs text-muted-foreground">{f.type}</TableCell>
                  <TableCell className="text-right text-xs">{Math.round(f.size / 1024)}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>

        {/* Mapped controls for each file */}
        {history.map(
          (f, idx) =>
            f.mappedControls &&
            f.mappedControls.length > 0 && (
              <div key={`mapped-${idx}`}>
                <MappedControlsTable data={f.mappedControls} />
              </div>
            ),
        )}
      </CardContent>
    </Card>
  )
}
