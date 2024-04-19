<template>
  <h2 class="text-primary mt-3">主要设计结果</h2>
  <div class="card mt-3 pt-3">
    <ol>
      <li>{{ mb.nums_info.total.module }}支{{ dr.module.model }}</li>
      <li>
        {{ mb.nums_info.total.train }}支{{
          mb.module_nums_per_train
        }}芯膜壳（即每{{ mb.module_nums_per_train }}只膜元件串联）
      </li>
      <li>
        系列{{ mb.serie_nums }}用{{ mb.serie_nums_backup }}备,
        {{ mb.group_nums_per_serie }}膜组/系列, 单组{{
          mb.arrange.result.join(":")
        }}*{{ mb.module_nums_per_train }}芯, {{ mb.install }}安装
      </li>

      <li>设计时间：{{ dr.real_info.hpd }}小时/天</li>
      <li>
        整体回收率：{{ numeral(dr.real_info.rec_net * 100).format("0.0") }}%
      </li>
      <li>运行回收率：{{ dr.main_balance.rec_operate * 100 }}%</li>
      <li>净通量：{{ numeral(dr.real_info.lmh_nominal).format("0.0") }}LMH</li>
      <li>
        运行通量：{{ numeral(dr.real_info.lmh_operate).format("0.0") }}LMH
      </li>
      <li>
        净产水量：{{ numeral(dr.real_info.perm_m3).format("0.0") }}m3/d ({{
          numeral(dr.real_info.perm_m3 / dr.real_info.hpd).format("0.0")
        }}m3/h)
      </li>
      <li>
        原水量{{ numeral(dr.real_info.raw_m3).format("0.0") }}m3/d ({{
          numeral(dr.real_info.raw_m3 / dr.real_info.hpd).format("0.0")
        }}m3/h)
      </li>
      <li>
        排放量：{{ numeral(dr.real_info.drain_m3).format("0.0") }}m3/d ({{
          numeral(dr.real_info.drain_m3 / dr.real_info.hpd).format("0.0")
        }}m3/h)
      </li>
      <li>详细结果请下载计算书或者报告查看。</li>
    </ol>
  </div>
</template>
<script>
import { inject, defineComponent } from "vue";
import { useStore } from "@/main";
export default defineComponent({
  setup() {
    const numeral = inject("numeral");
    const store = useStore();
    const storeLocal = inject("storeLocal");
    const urlName = inject("urlName");
    const dr = storeLocal.state.fd.design_result;
    const mb = dr.main_balance;
    return { storeLocal, store, urlName, dr, numeral, mb };
  },
});
</script>