<script>
  import { WordCloudChart } from '@carbon/charts-svelte';
  import '@carbon/styles/css/styles.css';
  import '@carbon/charts/styles.css';
  import axios from 'axios';

  let data = [];

  async function GetKeywordExtraction() {
    try {
      const response = await axios.get(`http://localhost:8000/analysis/own-keyword-extraction`);

      if (response.data) {
        data = response.data;
      }
    } catch (error) {
      console.log(error);
    }
  }

  $: GetKeywordExtraction();
</script>

<WordCloudChart
  {data}
  options={{
    title: 'Word cloud',
    resizable: true,
    color: {
      pairing: {
        option: 3
      }
    },
    height: '400px'
  }}
/>
