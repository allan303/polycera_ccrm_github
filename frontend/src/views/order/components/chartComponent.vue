<template>
  {{ lineChart }}
  <StandardListComponent
    :listScope="listScope"
    :urlModel="urlModel"
    :filter_dt_and="filter_dt_and"
    ref="child"
  >
    <div class="row">
      <MyCard bodyClass="text-center" col="4">
        <template v-slot:header> 最近7天 </template>
        <template v-slot:body>
          <h3 class="card-title pricing-card-title">
            新增 <strong class="text-primary">7</strong> 订单
          </h3>
          <h3 class="card-title pricing-card-title">
            金额 <strong class="text-primary">1,200,000</strong> RMB
          </h3>
          <ul class="list-unstyled mt-3 mb-4">
            <li>平均 <strong class="text-primary">3,000</strong> RMB/订单</li>
            <li>总计膜元件数量 <strong class="text-primary">200</strong> 支</li>
          </ul>
        </template>
      </MyCard>
      <MyCard bodyClass="text-center" col="4">
        <template v-slot:header> 最近30天 </template>
        <template v-slot:body>
          <h3 class="card-title pricing-card-title">
            新增 <strong class="text-primary">30</strong> 订单
          </h3>
          <h3 class="card-title pricing-card-title">
            金额 <strong class="text-primary">3,200,000</strong> RMB
          </h3>
          <ul class="list-unstyled mt-3 mb-4">
            <li>平均 <strong class="text-primary">3,000</strong> RMB/订单</li>
            <li>总计膜元件数量 <strong class="text-primary">200</strong> 支</li>
          </ul>
        </template>
      </MyCard>
      <MyCard bodyClass="text-center" col="4">
        <template v-slot:header> 最近90天 </template>
        <template v-slot:body>
          <h3 class="card-title pricing-card-title">
            新增 <strong class="text-primary">90</strong> 订单
          </h3>
          <h3 class="card-title pricing-card-title">
            金额 <strong class="text-primary">9,200,000</strong> RMB
          </h3>
          <ul class="list-unstyled mt-3 mb-4">
            <li>平均 <strong class="text-primary">3,000</strong> RMB/订单</li>
            <li>总计膜元件数量 <strong class="text-primary">200</strong> 支</li>
          </ul>
        </template>
      </MyCard>
    </div>
  </StandardListComponent>
</template>

<script>
import { computed, ref } from "vue";
import MyCard from "@/components/ui/MyCard";
import StandardListComponent from "@/components/StandardListComponent";

export default {
  name: "App",
  components: {
    MyCard,
    StandardListComponent,
  },
  props: {
    listScope: { required: true, type: String },
    urlModel: { type: String, default: null },
    filter_dt_and: { type: Object, default: null },
  },
  setup() {
    const child = ref({ value: {} });
    const createChart = (type, data) => {
      return {
        type: type || "bar",
        options: {
          // min: 0,
          // max: 100,
          responsive: true,
          plugins: {
            legend: {
              position: "top",
            },
          },
          parsing: {
            xAxisKey: "name",
            yAxisKey: "price",
          },
        },
        data: {
          datasets: [
            {
              label: "金额",
              backgroundColor: "#9b59b6",
              data: data,
            },
          ],
        },
      };
    };
    const barChart = createChart("bar", child.value.objs);
    const barData = computed(() => {
      return {
        datasets: [
          {
            label: "金额",
            backgroundColor: "#9b59b6",
            data: child.value.objs,
          },
        ],
      };
    });
    const lineChart = createChart("line", child.value.objs);

    return {
      barChart,
      lineChart,
      child,
      barData,
    };
  },
};
</script>
