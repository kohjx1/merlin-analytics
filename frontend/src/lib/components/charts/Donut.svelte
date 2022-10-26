<script>
	import { DonutChart } from "@carbon/charts-svelte";

	import "@carbon/styles/css/styles.css";
	import "@carbon/charts/styles.css";
</script>

<DonutChart
	data={[
	{
		"group": "2V2N 9KYPM version 1",
		"value": 20000
	},
	{
		"group": "L22I P66EP L22I P66EP L22I P66EP",
		"value": 65000
	},
	{
		"group": "JQAI 2M4L1",
		"value": 75000
	},
	{
		"group": "J9DZ F37AP",
		"value": 1200
	},
	{
		"group": "YEL48 Q6XK YEL48",
		"value": 10000
	},
	{
		"group": "Misc",
		"value": 25000
	}
]}
	options={{
	"title": "Donut",
	"resizable": true,
	"donut": {
		"center": {
			"label": "Browsers"
		}
	},
	"height": "400px"
}}
	/>
