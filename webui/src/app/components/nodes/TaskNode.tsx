import React from 'react'
import BaseNode, { BaseNodeProps } from './BaseNode'
import { Badge } from '../ui/badge'
import { NodeData } from '@/app/types';


function TaskNode({ data }: { data: NodeData }) {
  console.log('Rendering TaskNode', data);
  return (
    <BaseNode data={data}>
      <Badge variant="secondary">Input: {data.input || 'N/A'}</Badge>
    </BaseNode>
  )
}

export default TaskNode
