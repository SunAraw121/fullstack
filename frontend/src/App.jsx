import React, { useState } from 'react'
import LibraryPanel from './components/LibraryPanel.jsx'
import Workspace from './components/Workspace.jsx'
import ConfigPanel from './components/ConfigPanel.jsx'
import ExecutionBar from './components/ExecutionBar.jsx'
import Chat from './components/Chat.jsx'

export default function App() {
  const [nodes, setNodes] = useState([
    { id: '1', type: 'UserQuery', data: { label: 'User Query' }, position: { x: 100, y: 50 } },
    { id: '2', type: 'KnowledgeBase', data: { label: 'Knowledge Base' }, position: { x: 300, y: 150 } },
    { id: '3', type: 'LLMEngine', data: { label: 'LLM Engine' }, position: { x: 500, y: 250 } },
    { id: '4', type: 'Output', data: { label: 'Output' }, position: { x: 700, y: 350 } },
  ])

  const [edges, setEdges] = useState([])
  const [selected, setSelected] = useState(null)
  const [chatOpen, setChatOpen] = useState(false)
  const [graphName, setGraphName] = useState('My First Workflow')

  return (
    <div className="app">
      <div className="header">
        <h3 style={{ margin: 0 }}>Workflow Builder</h3>
        <span className="badge">React + React Flow</span>
        <span className="badge">FastAPI</span>
        <span className="badge">ChromaDB</span>
        <div style={{ marginLeft: 'auto' }}>
          <input value={graphName} onChange={e => setGraphName(e.target.value)} />
        </div>
      </div>

      <div className="library">
        <LibraryPanel setNodes={setNodes} />
      </div>

      <div className="workspace">
        <Workspace
          nodes={nodes}
          setNodes={setNodes}
          edges={edges}
          setEdges={setEdges}
          setSelected={setSelected}
        />
      </div>

      <div className="config">
        <ConfigPanel selected={selected} setNodes={setNodes} />
      </div>

      <div className="execbar">
        <ExecutionBar nodes={nodes} edges={edges} onOpenChat={() => setChatOpen(true)} />
      </div>

      <Chat open={chatOpen} onClose={() => setChatOpen(false)} nodes={nodes} edges={edges} />
    </div>
  )
}
