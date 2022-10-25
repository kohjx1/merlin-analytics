<script>
	import { DonutChart } from "@carbon/charts-svelte";
  import data from "../data/chart-store.js"

	import "@carbon/styles/css/styles.css";
	import "@carbon/charts/styles.css";

  let items;

  data.subscribe(its => {
    items = its
  })
</script>

<DonutChart
	data={items}
	options={{
	"resizable": true,
	"legend": {
		"alignment": "center"
	},
	"donut": {
		"center": {
			"label": "Browsers"
		},
		"alignment": "center"
	},
	"height": "400px"
}}
	/>