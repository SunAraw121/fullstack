import React, { useState } from 'react'
import api from '../api'

export default function Chat({ open, onClose, nodes, edges }){
  const [input, setInput] = useState('')
  const [log, setLog] = useState([])
  const send = async () => {
    if(!input.trim()) return
    setLog(l => [...l, {role:'user', content: input}])
    const res = await api.post('/workflow/run', { nodes, edges, query: input, debug: true })
    const text = res.data.ok ? res.data.answer : 'Error: ' + (res.data.errors||[]).join(', ')
    setLog(l => [...l, {role:'assistant', content: text}])
    setInput('')
  }
  return (
    <div className={'chat-modal ' + (open ? 'open':'' )}>
      <div className="chat-box">
        <div style={{display:'flex', alignItems:'center', gap:8}}>
          <h4 style={{margin:0}}>Chat with Stack</h4>
          <div style={{marginLeft:'auto'}}><button onClick={onClose}>Close</button></div>
        </div>
        <div className="chat-log">
          {log.map((m,i)=>(
            <div key={i} style={{whiteSpace:'pre-wrap', margin:'6px 0'}}><b>{m.role}:</b> {m.content}</div>
          ))}
        </div>
        <div className="chat-input">
          <input value={input} onChange={e=>setInput(e.target.value)} style={{flex:1}} placeholder="Ask a question..." />
          <button onClick={send}>Send</button>
        </div>
      </div>
    </div>
  )
}
