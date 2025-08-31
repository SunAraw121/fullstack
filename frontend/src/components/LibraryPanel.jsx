import React from 'react'

const items = [
  {type:'UserQuery', label:'User Query'},
  {type:'KnowledgeBase', label:'KnowledgeBase'},
  {type:'LLMEngine', label:'LLM Engine'},
  {type:'Output', label:'Output'},
]

export default function LibraryPanel({ setNodes }){
  const add = (type) => {
    const id = Math.random().toString(36).slice(2,8)
    setNodes(prev => [...prev, { id, type, position: { x: 100, y: 80 + prev.length*80 }, data: defaultData(type) } ])
  }
  return (
    <div>
      <h4>Components</h4>
      {items.map(it => (
        <div key={it.type} className="badge" style={{display:'inline-block', margin:'6px', cursor:'pointer'}} onClick={()=>add(it.type)}>
          {it.label}
        </div>
      ))}
      <p style={{fontSize:12, opacity:.8}}>Drag nodes around in the workspace, then connect them.</p>
    </div>
  )
}

function defaultData(type){
  switch(type){
    case 'KnowledgeBase': return { enabled: true, top_k: 4 }
    case 'LLMEngine': return { prompt: '', use_web: false }
    default: return {}
  }
}
