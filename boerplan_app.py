import { useState } from "react";
import { Line, Bar } from "recharts";
import { Card, CardContent } from "@/components/ui/card";
import { Select, SelectItem } from "@/components/ui/select";

const initialParams = {
  herdGrowthRate: 0.2,
  calvingRate: 0.8,
  replacementRate: 0.7,
  inflationRate: 0.047,
  cowCost: 14850,
};

const calculateData = (params) => {
  let years = 10;
  let data = [];
  let herdSize = 400;
  let cowCost = params.cowCost;
  
  for (let i = 0; i < years; i++) {
    herdSize *= 1 + params.herdGrowthRate;
    cowCost *= 1 + params.inflationRate;
    let totalCost = herdSize * cowCost;

    data.push({
      year: 2025 + i,
      herdSize: Math.round(herdSize),
      cowCost: Math.round(cowCost),
      totalCost: Math.round(totalCost),
    });
  }
  return data;
};

export default function BoerPlanApp() {
  const [params, setParams] = useState(initialParams);
  const data = calculateData(params);

  return (
    <div className="p-6 space-y-4">
      <h1 className="text-xl font-bold">BoerPlan Beta</h1>
      <Card>
        <CardContent>
          <Select
            onChange={(e) => setParams({ ...params, herdGrowthRate: parseFloat(e.target.value) })}
          >
            <SelectItem value="0.1">Herd Growth 10%</SelectItem>
            <SelectItem value="0.2">Herd Growth 20%</SelectItem>
            <SelectItem value="0.3">Herd Growth 30%</SelectItem>
          </Select>
        </CardContent>
      </Card>
      <Card>
        <CardContent>
          <Line data={data}>
            <Line type="monotone" dataKey="herdSize" stroke="#8884d8" />
            <Line type="monotone" dataKey="totalCost" stroke="#82ca9d" />
          </Line>
        </CardContent>
      </Card>
      <Card>
        <CardContent>
          <Bar data={data}>
            <Bar dataKey="herdSize" fill="#8884d8" />
            <Bar dataKey="totalCost" fill="#82ca9d" />
          </Bar>
        </CardContent>
      </Card>
    </div>
  );
}
