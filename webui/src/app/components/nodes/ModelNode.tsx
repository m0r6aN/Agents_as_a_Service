import React from 'react'
import BaseNode, { BaseNodeProps } from './BaseNode'
import { Badge } from '../ui/badge'
import { NodeData } from '@/app/types';

function ModelNode({ data }: { data: NodeData }) {
    console.log('Rendering ModelNode', data);
    return (
      <BaseNode data={data}>
        <Badge variant="secondary">URL: {data.inferenceUrl || 'N/A'}</Badge>
      </BaseNode>
    )
  }

export default ModelNode