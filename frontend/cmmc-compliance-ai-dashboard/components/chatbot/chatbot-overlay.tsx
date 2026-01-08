
// "use client"

// import { useEffect, useRef, useState } from "react"
// import { Button } from "@/components/ui/button"
// import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
// import { Card, CardContent } from "@/components/ui/card"
// import { Input } from "@/components/ui/input"

// type Msg = { role: "user" | "assistant"; content: string }

// export function ChatbotOverlay() {
//   const defaultMsg = "Hi! Ask about CMMC controls, gaps, or POA&M items."
//   const [open, setOpen] = useState(false)
//   const [messages, setMessages] = useState<Msg[]>([{ role: "assistant", content: defaultMsg }])
//   const [input, setInput] = useState("")
//   const [loading, setLoading] = useState(false)
//   const listRef = useRef<HTMLDivElement | null>(null)

//   useEffect(() => {
//     listRef.current?.scrollTo({ top: listRef.current.scrollHeight, behavior: "smooth" })
//   }, [messages.length, open])

//   const send = async () => {
//     if (!input.trim()) return
//     const userMsg = { role: "user", content: input.trim() } as Msg
//     setMessages((m) => [...m, userMsg])
//     setInput("")
//     setLoading(true)

//     try {
//       const res = await fetch("http://localhost:8000/api/chat", {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({ user_input: input.trim() }),
//       })
//       if (!res.ok) throw new Error("Backend error")
//       const data = await res.json()
//       const assistantMsg = { role: "assistant", content: data.response || defaultMsg } as Msg
//       setMessages((m) => [...m, assistantMsg])
//     } catch (err) {
//       // On error, show default assistant message
//       setMessages((m) => [...m, { role: "assistant", content: defaultMsg }])
//     } finally {
//       setLoading(false)
//     }
//   }

//   return (
//     <div className="fixed bottom-6 right-6 z-40">
//       <Dialog open={open} onOpenChange={setOpen}>
//         <DialogTrigger asChild>
//           <Button className="shadow-md">AI Chat</Button>
//         </DialogTrigger>
//         <DialogContent className="max-w-2xl">
//           <DialogHeader>
//             <DialogTitle className="text-sm">AI Chatbot</DialogTitle>
//           </DialogHeader>
//           <Card className="flex h-[60dvh] flex-col">
//             <CardContent className="flex min-h-0 flex-1 flex-col gap-3 p-3">
//               <div
//                 ref={listRef}
//                 className="scrollbar-thin flex-1 space-y-3 overflow-auto rounded-md border p-3"
//               >
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
//                 {loading && (
//                   <div className="flex justify-start">
//                     <div className="max-w-[70%] rounded-lg bg-accent px-3 py-2 text-sm opacity-70">
//                       Thinking...
//                     </div>
//                   </div>
//                 )}
//               </div>
//               <div className="flex gap-2">
//                 <Input
//                   placeholder="Ask about controls, evidence, or gaps..."
//                   value={input}
//                   onChange={(e) => setInput(e.target.value)}
//                   onKeyDown={(e) => e.key === "Enter" && send()}
//                   disabled={loading}
//                 />
//                 <Button onClick={send} disabled={loading}>
//                   Send
//                 </Button>
//               </div>
//             </CardContent>
//           </Card>
//         </DialogContent>
//       </Dialog>
//     </div>
//   )
// }


"use client"

import { useEffect, useRef, useState } from "react"
import { Button } from "@/components/ui/button"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import { Card, CardContent } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm"

type Msg = { role: "user" | "assistant"; content: string }

export function ChatbotOverlay() {
  const defaultMsg = "Hi! Ask about CMMC controls, gaps, or POA&M items."
  const [open, setOpen] = useState(false)
  const [messages, setMessages] = useState<Msg[]>([{ role: "assistant", content: defaultMsg }])
  const [input, setInput] = useState("")
  const [loading, setLoading] = useState(false)
  const listRef = useRef<HTMLDivElement | null>(null)

  useEffect(() => {
    listRef.current?.scrollTo({ top: listRef.current.scrollHeight, behavior: "smooth" })
  }, [messages.length, open])

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
      setMessages((m) => [...m, { role: "assistant", content: defaultMsg }])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="fixed bottom-6 right-6 z-40">
      <Dialog open={open} onOpenChange={setOpen}>
        <DialogTrigger asChild>
          <Button className="shadow-md">AI Chat</Button>
        </DialogTrigger>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle className="text-sm">AI Chatbot</DialogTitle>
          </DialogHeader>
          <Card className="flex h-[60dvh] flex-col">
            <CardContent className="flex min-h-0 flex-1 flex-col gap-3 p-3">
              <div
                ref={listRef}
                className="scrollbar-thin flex-1 space-y-3 overflow-auto rounded-md border p-3"
              >
                {messages.map((m, i) => (
                  <div key={i} className={m.role === "user" ? "flex justify-end" : "flex justify-start"}>
                    <div
                      className={
                        m.role === "user"
                          ? "max-w-[70%] rounded-lg bg-primary px-3 py-2 text-primary-foreground text-sm"
                          : "max-w-[70%] rounded-lg bg-accent px-3 py-2 text-sm"
                      }
                    >
                      <ReactMarkdown
                        remarkPlugins={[remarkGfm]}
                        components={{
                          p: ({ node, ...props }) => <p className="m-0 whitespace-pre-wrap" {...props} />,
                          a: ({ node, ...props }) => (
                            <a {...props} target="_blank" rel="noopener noreferrer" className="underline text-primary-foreground" />
                          ),
                          strong: ({ node, ...props }) => <strong className="font-semibold" {...props} />,
                          em: ({ node, ...props }) => <em className="italic" {...props} />,
                          code: ({ node, ...props }) => <code className="bg-gray-200 px-1 rounded text-sm" {...props} />,
                        }}
                      >
                        {m.content}
                      </ReactMarkdown>
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
              <div className="flex gap-2 mt-2">
                <Input
                  placeholder="Ask about controls, evidence, or gaps..."
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={(e) => e.key === "Enter" && send()}
                  disabled={loading}
                  className="flex-1"
                />
                <Button onClick={send} disabled={loading}>
                  Send
                </Button>
              </div>
            </CardContent>
          </Card>
        </DialogContent>
      </Dialog>
    </div>
  )
}
