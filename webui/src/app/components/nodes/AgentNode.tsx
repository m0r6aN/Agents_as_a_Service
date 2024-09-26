import React from 'react'
import BaseNode, { BaseNodeProps } from './BaseNode'
import { Badge } from '../ui/badge'
import { NodeData } from '@/app/types';

function AgentNode({ data }: { data: NodeData }) {
    console.log('Rendering AgentNode', data);
    return (
      <BaseNode data={data}>
        <Badge variant="secondary">Model: {data.model || 'N/A'}</Badge>
      </BaseNode>
    )
  }

export default AgentNode