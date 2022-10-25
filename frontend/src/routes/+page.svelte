<script>
  import WordCloud from "../components/charts/WordCloud.svelte"
  import DonutChart from "../components/charts/DonutChart.svelte"
  import Grid from "svelte-grid-responsive"
</script>

<h2>Data Analytics</h2>

<br/>

<Grid container>
  <Grid xs={8} md={8} lg={8}>
    <WordCloud />
  </Grid>
  <Grid xs={4} md={4} lg={4}>
    <DonutChart />
  </Grid>
</Grid>