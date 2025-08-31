import React, { useCallback } from 'react'
import ReactFlow, { addEdge, Background, Controls } from 'react-flow-renderer'
import NodeUserQuery from './nodes/NodeUserQuery.jsx'
import NodeKnowledgeBase from './nodes/NodeKnowledgeBase.jsx'
import NodeLLMEngine from './nodes/NodeLLMEngine.jsx'
import NodeOutput from './nodes/NodeOutput.jsx'

const nodeTypes = {
  UserQuery: NodeUserQuery,
  KnowledgeBase: NodeKnowledgeBase,
  LLMEngine: NodeLLMEngine,
  Output: NodeOutput
}

export default function Workspace({ nodes, setNodes, edges, setEdges, setSelected }){
  const onConnect = useCallback((params)=> setEdges(eds => addEdge(params, eds)), [])
  const onNodesChange = changes => {
    setNodes(nds => nds.map(n => {
      const ch = changes.find(c => c.id === n.id && c.type === 'position')
      return ch ? {...n, position: ch.position} : n
    }))
  }
  const onSelectionChange = ({ nodes: sel }) => setSelected(sel && sel[0] ? sel[0] : null)
  return (
    <div style={{height:'100%'}}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onConnect={onConnect}
        onNodesChange={onNodesChange}
        onSelectionChange={onSelectionChange}
        nodeTypes={nodeTypes}
        fitView
      >
        <Background />
        <Controls />
      </ReactFlow>
    </div>
  )
}
