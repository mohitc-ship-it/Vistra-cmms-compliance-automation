// "use client"

// import AppShell from "@/components/app-shell"
// import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
// import { Input } from "@/components/ui/input"
// import { Button } from "@/components/ui/button"
// import { useEffect, useRef, useState } from "react"
// import { motion } from "framer-motion"

// type Msg = { role: "user" | "assistant"; content: string }

// const contextSummaries = [
//   { id: "AC.L1-3.1.1", summary: "Access limited to authorized users. Evidence: AD group policy." },
//   { id: "IA.L2-3.5.3", summary: "MFA required for remote and admin access. Gap: contractors." },
// ]

// export default function ChatbotPage() {
//   const [messages, setMessages] = useState<Msg[]>([
//     { role: "assistant", content: "Hello! Ask about your CMMC controls, gaps, or POA&M status." },
//   ])
//   const [input, setInput] = useState("")
//   const listRef = useRef<HTMLDivElement | null>(null)

//   useEffect(() => {
//     listRef.current?.scrollTo({ top: listRef.current.scrollHeight, behavior: "smooth" })
//   }, [messages.length])

//   const send = () => {
//     if (!input.trim()) return
//     const user = { role: "user", content: input.trim() } as Msg
//     setMessages((m) => [...m, user])
//     setInput("")

//     // Simulated streaming line-by-line
//     const lines = [
//       "Analyzing mapped controls...",
//       "Cross-referencing POA&M items...",
//       "Noted MFA gap for contractor access (IA.L2-3.5.3).",
//       "Recommend enabling conditional access policy with MFA.",
//     ]
//     let i = 0
//     const id = setInterval(() => {
//       setMessages((m) => {
//         const last = m[m.length - 1]
//         if (last?.role === "assistant" && last.content.startsWith("Analyzing")) {
//           // append more to streaming msg
//           const updated = [...m]
//           updated[updated.length - 1] = { role: "assistant", content: lines.slice(0, i + 1).join("\n") }
//           i++
//           if (i >= lines.length) clearInterval(id)
//           return updated
//         }
//         // start stream
//         return [...m, { role: "assistant", content: lines[0] }]
//       })
//       if (i >= lines.length) clearInterval(id)
//     }, 350)
//   }

//   return (
//     <AppShell>
//       <motion.div initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }}>
//         <div className="grid gap-6 lg:grid-cols-[280px_1fr]">
//           <Card className="hidden lg:block">
//             <CardHeader>
//               <CardTitle className="text-sm">Context</CardTitle>
//             </CardHeader>
//             <CardContent className="grid gap-3">
//               {contextSummaries.map((c) => (
//                 <div key={c.id} className="rounded-md border p-3">
//                   <div className="text-xs font-mono text-muted-foreground">{c.id}</div>
//                   <div className="text-sm">{c.summary}</div>
//                 </div>
//               ))}
//             </CardContent>
//           </Card>

//           <Card className="flex h-[70dvh] flex-col">
//             <CardHeader>
//               <CardTitle className="text-sm">AI Chatbot</CardTitle>
//             </CardHeader>
//             <CardContent className="flex min-h-0 flex-1 flex-col gap-3">
//               <div ref={listRef} className="scrollbar-thin flex-1 space-y-3 overflow-auto rounded-md border p-3">
//                 {messages.map((m, i) => (
//                   <div key={i} className={m.role === "user" ? "flex justify-end" : "flex justify-start"}>
//                     <div
//                       className={
//                         m.role === "user"
//                           ? "max-w-[70%] rounded-lg bg-primary px-3 py-2 text-primary-foreground"
//                           : "max-w-[70%] rounded-lg bg-accent px-3 py-2"
//                       }
//                     >
//                       <pre className="whitespace-pre-wrap text-sm">{m.content}</pre>
//                     </div>
//                   </div>
//                 ))}
//               </div>
//               <div className="flex gap-2">
//                 <Input
//                   placeholder="Ask about controls, evidence, or gaps..."
//                   value={input}
//                   onChange={(e) => setInput(e.target.value)}
//                   onKeyDown={(e) => e.key === "Enter" && send()}
//                 />
//                 <Button onClick={send}>Send</Button>
//               </div>
//             </CardContent>
//           </Card>
//         </div>
//       </motion.div>
//     </AppShell>
//   )
// }

"use client"

import AppShell from "@/components/app-shell"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { useEffect, useRef, useState } from "react"
import { motion } from "framer-motion"

type Msg = { role: "user" | "assistant"; content: string }

const contextSummaries = [
  { id: "AC.L1-3.1.1", summary: "Access limited to authorized users. Evidence: AD group policy." },
  { id: "IA.L2-3.5.3", summary: "MFA required for remote and admin access. Gap: contractors." },
]

export default function ChatbotPage() {
  const defaultMsg = "Hello! Ask about your CMMC controls, gaps, or POA&M status."
  const [messages, setMessages] = useState<Msg[]>([{ role: "assistant", content: defaultMsg }])
  const [input, setInput] = useState("")
  const [loading, setLoading] = useState(false)
  const listRef = useRef<HTMLDivElement | null>(null)

  useEffect(() => {
    listRef.current?.scrollTo({ top: listRef.current.scrollHeight, behavior: "smooth" })
  }, [messages.length])

  const send = async () => {
    if (!input.trim()) return
    const userMsg = { role: "user", content: input.trim() } as Msg
    setMessages((m) => [...m, userMsg])
    setInput("")
    setLoading(true)

    try {
      const res = await fetch("http://localhost:8000/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_input: input.trim() }),
      })
      if (!res.ok) throw new Error("Backend error")
      const data = await res.json()
      const assistantMsg = { role: "assistant", content: data.response || defaultMsg } as Msg
      setMessages((m) => [...m, assistantMsg])
    } catch (err) {
      // On error, show default assistant message
      setMessages((m) => [...m, { role: "assistant", content: defaultMsg }])
    } finally {
      setLoading(false)
    }
  }

  return (
    <AppShell>
      <motion.div initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }}>
        <div className="grid gap-6 lg:grid-cols">
          {/* Context Panel */}
          {/* <Card className="hidden lg:block">
            <CardHeader>
              <CardTitle className="text-sm">Context</CardTitle>
            </CardHeader>
            <CardContent className="grid gap-3">
              {contextSummaries.map((c) => (
                <div key={c.id} className="rounded-md border p-3">
                  <div className="text-xs font-mono text-muted-foreground">{c.id}</div>
                  <div className="text-sm">{c.summary}</div>
                </div>
              ))}
            </CardContent>
          </Card> */}

          {/* Chatbot Panel */}
          <Card className="flex h-[70dvh] flex-col">
            <CardHeader>
              <CardTitle className="text-sm">AI Chatbot</CardTitle>
            </CardHeader>
            <CardContent className="flex min-h-0 flex-1 flex-col gap-3">
              <div
                ref={listRef}
                className="scrollbar-thin flex-1 space-y-3 overflow-auto rounded-md border p-3"
              >
                {messages.map((m, i) => (
                  <div key={i} className={m.role === "user" ? "flex justify-end" : "flex justify-start"}>
                    <div
                      className={
                        m.role === "user"
                          ? "max-w-[70%] rounded-lg bg-primary px-3 py-2 text-primary-foreground"
                          : "max-w-[70%] rounded-lg bg-accent px-3 py-2"
                      }
                    >
                      <pre className="whitespace-pre-wrap text-sm">{m.content}</pre>
                    </div>
                  </div>
                ))}
                {loading && (
                  <div className="flex justify-start">
                    <div className="max-w-[70%] rounded-lg bg-accent px-3 py-2 text-sm opacity-70">
                      Thinking...
                    </div>
                  </div>
                )}
              </div>
              <div className="flex gap-2">
                <Input
                  placeholder="Ask about controls, evidence, or gaps..."
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={(e) => e.key === "Enter" && send()}
                  disabled={loading}
                />
                <Button onClick={send} disabled={loading}>
                  Send
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </motion.div>
    </AppShell>
  )
}
