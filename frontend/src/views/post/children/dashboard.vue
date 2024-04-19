<template>
  <div style="width: 400px">
    <div style="display: flex; justify-content: center">
      <button type="button" @click="shuffleData">Shuffle</button>
      <button type="button" @click="switchLegend">Swicth legends</button>
    </div>
    <BarChart v-bind="barChartProps" />
  </div>
</template>

<script >
import { computed, ref } from "vue";
import { shuffle } from "lodash";
import { BarChart, useBarChart } from "vue-chart-3";

// Chart.register(...registerables);

export default {
  name: "App",
  components: { BarChart },
  setup() {
    const dataValues = ref([30, 40, 60, 70, 5]);
    const toggleLegend = ref(true);

    const testData = computed(() => ({
      labels: ["Paris", "Nîmes", "Toulon", "Perpignan", "Autre"],
      datasets: [
        {
          data: dataValues.value,
          backgroundColor: [
            "#77CEFF",
            "#0079AF",
            "#123E6B",
            "#97B0C4",
            "#A5C8ED",
          ],
        },
      ],
    }));

    const options = computed(() => ({
      scales: {
        myScale: {
          type: "logarithmic",
          position: toggleLegend.value ? "left" : "right",
        },
      },
      plugins: {
        legend: {
          position: toggleLegend.value ? "top" : "bottom",
        },
        title: {
          display: true,
          text: "Chart.js Doughnut Chart",
        },
      },
    }));

    const { barChartProps, barChartRef } = useBarChart({
      chartData: testData,
      options,
    });

    function shuffleData() {
      dataValues.value = shuffle(dataValues.value);
      console.log(barChartRef.value.chartInstance);
    }

    function switchLegend() {
      toggleLegend.value = !toggleLegend.value;
    }

    return {
      shuffleData,
      switchLegend,
      testData,
      options,
      barChartRef,
      barChartProps,
    };
  },
};
</script>
