import {
  PieChart as RechartsPieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';

interface PieChartProps {
  data: { name: string; value: number }[];
  height?: number;
  innerRadius?: number;
  colors?: string[];
  showLegend?: boolean;
}

const DEFAULT_COLORS = [
  '#2563eb',
  '#16a34a',
  '#ca8a04',
  '#dc2626',
  '#9333ea',
  '#0891b2',
  '#c026d3',
  '#ea580c',
];

export default function PieChart({
  data,
  height = 300,
  innerRadius = 0,
  colors = DEFAULT_COLORS,
  showLegend = true,
}: PieChartProps) {
  return (
    <ResponsiveContainer width="100%" height={height}>
      <RechartsPieChart>
        <Pie
          data={data}
          cx="50%"
          cy="50%"
          innerRadius={innerRadius}
          outerRadius={80}
          fill="#8884d8"
          dataKey="value"
          label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
        >
          {data.map((_, index) => (
            <Cell key={`cell-${index}`} fill={colors[index % colors.length]} />
          ))}
        </Pie>
        <Tooltip />
        {showLegend && <Legend />}
      </RechartsPieChart>
    </ResponsiveContainer>
  );
}
