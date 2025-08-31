import React from 'react'

export default function ConfigPanel({ selected, setNodes }){
  if(!selected) return <div><h4>Config</h4><p>Select a node to edit its configuration.</p></div>

  const update = (patch) => {
    setNodes(prev => prev.map(n => n.id === selected.id ? {...n, data:{...n.data, ...patch}} : n))
  }

  if(selected.type === 'KnowledgeBase'){
    return (
      <div>
        <h4>KnowledgeBase</h4>
        <label><input type="checkbox" checked={!!selected.data.enabled} onChange={e=>update({enabled:e.target.checked})} /> enabled</label>
        <div>top_k: <input type="number" value={selected.data.top_k} onChange={e=>update({top_k:Number(e.target.value)})} /></div>
        <hr />
        <UploadBox />
      </div>
    )
  }
  if(selected.type === 'LLMEngine'){
    return (
      <div>
        <h4>LLM Engine</h4>
        <div>custom prompt:</div>
        <textarea rows="6" style={{width:'100%'}} value={selected.data.prompt||''} onChange={e=>update({prompt:e.target.value})} />
        <label><input type="checkbox" checked={!!selected.data.use_web} onChange={e=>update({use_web:e.target.checked})} /> use web search</label>
      </div>
    )
  }
  return <div><h4>{selected.type}</h4><p>No specific options.</p></div>
}

import api from '../api'
function UploadBox(){
  const onChange = async (e) => {
    const f = e.target.files[0]
    if(!f) return
    const form = new FormData()
    form.append('file', f)
    const res = await api.post('/documents/upload', form, { headers: { 'Content-Type': 'multipart/form-data' } })
    alert('Uploaded! Pages: '+res.data.pages+' Chunks: '+res.data.chunks)
  }
  return <div><input type="file" accept="application/pdf" onChange={onChange} /></div>
}
