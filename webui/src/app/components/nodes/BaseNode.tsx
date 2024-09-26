import React from 'react'
import { Handle, Position } from 'reactflow'
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

export interface BaseNodeProps {
  data: {
    label: string
    name: string
    description: string
    [key: string]: any
  }
}

function BaseNode({ data, children }: React.PropsWithChildren<BaseNodeProps>) {
  return (
    <Card className="w-[250px]">
      <CardHeader className="pb-2">
        <CardTitle className="text-md">{data.name || data.label}</CardTitle>
      </CardHeader>
      <CardContent>
        <p className="text-sm text-muted-foreground mb-2">{data.description}</p>
        {children}
      </CardContent>
      <Handle type="target" position={Position.Top} className="w-16 !bg-muted-foreground" />
      <Handle type="source" position={Position.Bottom} className="w-16 !bg-muted-foreground" />
    </Card>
  )
}   

export default BaseNode
