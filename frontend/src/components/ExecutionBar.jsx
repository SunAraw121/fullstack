import React from 'react'
import api from '../api'

export default function ExecutionBar({ nodes, edges, onOpenChat }){
  const build = async () => {
    // Very lightweight client-side validation
    const types = nodes.map(n=>n.type)
    if(types[0] !== 'UserQuery') return alert('First node should be UserQuery')
    if(types[types.length-1] !== 'Output') return alert('Last node should be Output')
    if(!types.includes('LLMEngine')) return alert('LLM Engine required')
    alert('Build OK. You can now open Chat with Stack.')
  }

  return (
    <>
      <button onClick={build}>Build Stack</button>
      <button onClick={onOpenChat}>Chat with Stack</button>
    </>
  )
}
