"use client"

import { useState, useRef, useCallback, useMemo } from "react"
import { useDropzone } from "react-dropzone"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { useToast } from "@/hooks/use-toast"

type UploadedFile = { file: File }
type MappedControl = { id: string; confidence: number; summary: string; docName: string; date: string }
type UploadedHistory = { file: UploadedFile; mappedControls: MappedControl[] }

// Fallback mock data
const EXAMPLE_HISTORY: UploadedHistory[] = [
  {
    file: { file: new File([], "Policies.pdf") },
    mappedControls: [
      { id: "03.01.10.c", confidence: 0.92, summary: "Previously visible info concealed after inactivity.", docName: "Policies.pdf", date: "2025-10-19" },
      { id: "03.01.11.a", confidence: 0.81, summary: "User session termination conditions defined.", docName: "Policies.pdf", date: "2025-10-19" },
      { id: "03.01.11.b", confidence: 0.88, summary: "User session automatically terminated when conditions occur.", docName: "Policies.pdf", date: "2025-10-19" },
      { id: "03.01.12.a", confidence: 0.79, summary: "Remote access sessions permitted.", docName: "Policies.pdf", date: "2025-10-19" },
    ],
  },
  {
    file: { file: new File([], "Procedures.docx") },
    mappedControls: [
      { id: "03.01.12.b", confidence: 0.85, summary: "Types of permitted remote access are identified.", docName: "Procedures.docx", date: "2025-10-18" },
      { id: "03.01.12.c", confidence: 0.73, summary: "Remote access sessions are controlled.", docName: "Procedures.docx", date: "2025-10-18" },
      { id: "03.01.13.a", confidence: 0.90, summary: "Cryptographic mechanisms protect confidentiality of remote sessions.", docName: "Procedures.docx", date: "2025-10-18" },
    ],
  },
  {
    file: { file: new File([], "Guidelines.xlsx") },
    mappedControls: [
      { id: "03.01.14.a", confidence: 0.80, summary: "Access control policies are reviewed regularly.", docName: "Guidelines.xlsx", date: "2025-10-17" },
      { id: "03.01.15.a", confidence: 0.77, summary: "User roles are defined and enforced.", docName: "Guidelines.xlsx", date: "2025-10-17" },
      { id: "03.01.16.a", confidence: 0.92, summary: "Audit logs maintained and reviewed.", docName: "Guidelines.xlsx", date: "2025-10-17" },
      { id: "03.01.17.a", confidence: 0.69, summary: "Remote access requires MFA.", docName: "Guidelines.xlsx", date: "2025-10-17" },
    ],
  },
]


export function UploadBox() {
  const [files, setFiles] = useState<UploadedFile[]>([])
  const [history, setHistory] = useState<UploadedHistory[]>(EXAMPLE_HISTORY)
  const [loading, setLoading] = useState(false)
  const [search, setSearch] = useState("")
  const inputRef = useRef<HTMLInputElement | null>(null)
  const { toast } = useToast()

  // Dropzone
  const onDropAccepted = useCallback((acceptedFiles: File[]) => {
    const newFiles = acceptedFiles.map((f) => ({ file: f }))
    setFiles((prev) => [...prev, ...newFiles])
  }, [])

  const { getRootProps, getInputProps, isDragActive, isDragReject } = useDropzone({
    onDropAccepted,
    multiple: true,
    accept: {
      "application/pdf": [".pdf"],
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document": [".docx"],
      "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": [".xlsx"],
    },
    noClick: true,
  })

  const onSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selected = Array.from(e.target.files || []).map((f) => ({ file: f }))
    setFiles((prev) => [...prev, ...selected])
    if (inputRef.current) inputRef.current.value = ""
  }

  const badgeVariant = (confidence: number) => {
    if (confidence >= 0.9) return "default"
    if (confidence >= 0.75) return "secondary"
    return "destructive"
  }

  // Map files via API
  const mapFiles = async () => {
    if (files.length === 0) {
      toast({ title: "No files", description: "Please upload files before mapping." })
      return
    }

    setLoading(true)
    try {
      const newHistory: UploadedHistory[] = []

      for (const f of files) {
        const formData = new FormData()
        formData.append("file", f.file)

        const res = await fetch("http://localhost:8000/api/map-file", {
          method: "POST",
          body: formData,
        })

        if (!res.ok) throw new Error(`API returned ${res.status}`)

        const data: { mappedControls: MappedControl[] } = await res.json()

        newHistory.push({
          file: f,
          mappedControls: data.mappedControls.map((c) => ({ ...c, docName: f.file.name, date: new Date().toISOString().split("T")[0] })),
        })
      }

      setHistory((prev) => [...newHistory, ...prev])
      setFiles([])
      toast({ title: "Mapping done", description: "Files mapped successfully via API." })
    } catch (err) {
      console.error("API mapping failed:", err)
      toast({ title: "API Error", description: "Mapping API failed. Using mock data." })

      // fallback mock data
      const fallback: UploadedHistory[] = files.map((f) => ({
        file: f,
        mappedControls: [
          {
            id: "03.01.XX",
            confidence: Math.random() * 0.3 + 0.7,
            summary: "Mapped using fallback mock",
            docName: f.file.name,
            date: new Date().toISOString().split("T")[0],
          },
        ],
      }))

      setHistory((prev) => [...fallback, ...prev])
      setFiles([])
    } finally {
      setLoading(false)
    }
  }

  const flattenedControls = useMemo(() => {
    return history
      .flatMap((h) => h.mappedControls)
      .filter((c) => c.summary.toLowerCase().includes(search.toLowerCase()) || c.id.toLowerCase().includes(search.toLowerCase()))
  }, [history, search])

  return (
    <div className="grid md:grid-cols-2 gap-6">
      {/* History Table */}
      <Card>
        <CardHeader className="flex justify-between items-center">
          <CardTitle className="text-sm">History & Mappings</CardTitle>
          <Input
            placeholder="Search Control ID / Summary"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="max-w-xs text-sm"
          />
        </CardHeader>
        <CardContent className="overflow-auto max-h-[60vh]">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Control ID</TableHead>
                <TableHead>Doc Name</TableHead>
                <TableHead>Summary</TableHead>
                <TableHead className="text-right">Confidence</TableHead>
                <TableHead>Date</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {flattenedControls.map((c, i) => (
                <TableRow key={`${c.docName}-${i}`}>
                  <TableCell className="text-sm">{c.id}</TableCell>
                  <TableCell className="text-sm">{c.docName}</TableCell>
                  <TableCell className="text-sm break-words">{c.summary}</TableCell>
                  <TableCell className="text-right text-sm">
                    <Badge variant={badgeVariant(c.confidence)}>{Math.round(c.confidence * 100)}%</Badge>
                  </TableCell>
                  <TableCell className="text-sm">{c.date}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>

      {/* Upload Panel */}
      <Card>
        <CardHeader>
          <CardTitle className="text-sm">Upload Documents</CardTitle>
        </CardHeader>
        <CardContent className="grid gap-4">
          <div
            {...getRootProps()}
            className={[
              "grid place-items-center rounded-lg border border-dashed p-8 text-center transition-colors",
              "bg-card/50",
              isDragActive ? "border-primary/60 bg-primary/5" : "border-border",
              isDragReject ? "border-destructive/60" : "",
            ].join(" ")}
          >
            <input {...getInputProps()} />
            <div className="grid gap-2">
              <p className="text-sm">
                {isDragReject
                  ? "Unsupported file type"
                  : isDragActive
                  ? "Drop files to upload"
                  : "Drag and drop files here"}
              </p>
              <p className="text-xs text-muted-foreground">PDF, DOCX, XLSX supported</p>
              <div className="flex items-center justify-center gap-2">
                <Button onClick={() => inputRef.current?.click()}>Select Files</Button>
                <input ref={inputRef} type="file" multiple className="hidden" onChange={onSelect} />
              </div>
            </div>
          </div>

          {files.length > 0 && (
            <div className="grid gap-2">
              {files.map((f) => (
                <div key={f.file.name} className="flex justify-between items-center border rounded p-2">
                  <span className="text-sm">{f.file.name}</span>
                  <span className="text-xs text-muted-foreground">{Math.round(f.file.size / 1024)} KB</span>
                </div>
              ))}
              <div className="flex justify-end">
                <Button onClick={mapFiles} disabled={loading}>
                  {loading ? "Mapping..." : "Map Files"}
                </Button>
              </div>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
