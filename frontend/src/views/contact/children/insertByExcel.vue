<template>
  <div class="row">
    <div class="col-12">
      <h3>Excel格式说明</h3>
      <ol>
        <li>用于一次性导入多个联系人信息</li>
        <li>单个sheet的Excel文件(.xlsx)，第一行为表头</li>
        <li>表头可以缺失（比如没有title职位一列），但是必须有联系人姓名</li>
        <li>表头对应如下表：</li>
      </ol>
    </div>
    <div class="clo-12">
      <table class="table table-bold">
        <thead>
          <tr>
            <th>内容</th>
            <th>表头字段</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>联系人姓名</td>
            <td>name</td>
          </tr>
          <tr>
            <td>公司名称</td>
            <td>new_oemname</td>
          </tr>
          <tr>
            <td>公司类型</td>
            <td>new_oemtype</td>
          </tr>
          <tr>
            <td>部门</td>
            <td>department</td>
          </tr>
          <tr>
            <td>职位</td>
            <td>title</td>
          </tr>
          <tr>
            <td>电话</td>
            <td>phone</td>
          </tr>
          <tr>
            <td>地址</td>
            <td>address</td>
          </tr>
          <tr>
            <td>邮箱</td>
            <td>email</td>
          </tr>
          <tr>
            <td>备注</td>
            <td>remark</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
  <form action="">
    <div class="input-group mb-3">
      <label class="input-group-text" for="inputGroupFile01"
        >标准Excel文件(小于2m)</label
      >

      <input
        type="file"
        class="form-control"
        id="inputGroupFile01"
        @change="getFile($event)"
      />
    </div>
    <button class="btn btn-primary mt-3" @click="uploadFile(file)">
      {{ $t("actions.submit") }}
    </button>
  </form>
</template>

<script scope>
// import FormInput from "@/components/ui/FormInput";
import { useAxios } from "@/main";
import { ref } from "vue";
export default {
  components: {
    // FormInput,
  },
  setup() {
    const axios = useAxios();
    const file = ref(null);
    const getFile = (event) => {
      file.value = event.target.files[0];
      console.log(file.value);
    };
    const beforeUpload = (file) => {
      const size = file.size;
      if (size / 1024 / 1024 > 2) {
        alert("文件>2m");
        return false;
      }
      return true;
    };
    const uploadFile = (file) => {
      if (!file) {
        return false;
      }
      if (!beforeUpload(file)) {
        return false;
      }
      const param = new FormData();
      param.append("file", file);
      console.log(param);
      const config = {
        headers: { "Content-Type": "multipart/form-data" },
      };
      axios.post("/contact/insert-by-excel", param, config).then((res) => {
        console.log(res.data);
        alert(
          `成功新增${res.data.i.length}个联系人，忽略或错误${res.data.ei.length}个联系人`
        );
      });
    };
    return { uploadFile, file, getFile };
  },
};
</script>
