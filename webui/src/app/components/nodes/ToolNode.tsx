import React from 'react'
import BaseNode, { BaseNodeProps } from './BaseNode'
import { Badge } from '../ui/badge'
import { NodeData } from '@/app/types';

function ToolNode({ data }: { data: NodeData }) {
    console.log('Rendering ToolNode', data);
    return (
      <BaseNode data={data}>
        <Badge variant="secondary">Function: {data.function || 'N/A'}</Badge>
      </BaseNode>
    )
  }

export default ToolNode