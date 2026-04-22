import {
  LineChart as RechartsLineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';

interface LineConfig {
  dataKey: string;
  name: string;
  color: string;
}

interface LineChartProps {
  data: Record<string, unknown>[];
  xDataKey: string;
  lines: LineConfig[];
  height?: number;
  showGrid?: boolean;
  showLegend?: boolean;
}

export default function LineChart({
  data,
  xDataKey,
  lines,
  height = 300,
  showGrid = true,
  showLegend = true,
}: LineChartProps) {
  return (
    <ResponsiveContainer width="100%" height={height}>
      <RechartsLineChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
        {showGrid && <CartesianGrid strokeDasharray="3 3" />}
        <XAxis dataKey={xDataKey} />
        <YAxis />
        <Tooltip />
        {showLegend && <Legend />}
        {lines.map((line) => (
          <Line
            key={line.dataKey}
            type="monotone"
            dataKey={line.dataKey}
            name={line.name}
            stroke={line.color}
            strokeWidth={2}
            dot={{ r: 4 }}
            activeDot={{ r: 6 }}
          />
        ))}
      </RechartsLineChart>
    </ResponsiveContainer>
  );
}
