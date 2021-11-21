<template>
  <a-modal v-model="visible" title="规格设置" :maskClosable="false" okText="确定" cancelText="取消" @ok="confirm"
    @cancel="$emit('cancel')">
    <div>
      <div style="margin-bottom: 12px;">规格分类:</div>
      <a-select v-model="specClsId" @change="changeSpecCls" style="width: 100%;" allowClear>
        <a-select-option v-for="item in specClsItems" :key="item.id" :value="item.id">
          {{item.name}}
        </a-select-option>
      </a-select>
    </div>
    <div style="margin-top: 12px;">
      <div style="margin-bottom: 12px;">规格:</div>
      <a-checkbox-group v-model="checkedSpec">
        <a-checkbox v-for="item in selectedSpecCls.spec_list" :key="item.id" :value="item.id">{{item.name}}</a-checkbox>
      </a-checkbox-group>
    </div>
  </a-modal>
</template>

<script>
  export default {
    name: 'SpecModal',
    props: ['visible', 'specClsItems', 'checkedSpec'],
    data() {
      return {
        specClsId: '',
        selectedSpecCls: {},
      };
    },
    methods: {
      changeSpecCls(value) {
        this.checkedSpec = [];

        if (!value) {
          this.selectedSpecCls = {};
          return
        }

        for (let specCls of this.specClsItems) {
          if (specCls.id === value) {
            this.selectedSpecCls = specCls;
            break
          }
        }
      },
      confirm() {
        if (this.selectedSpecCls.spec_list) {
          let specName = [];
          for (let item of this.selectedSpecCls.spec_list) {
            for (let spec_id of this.checkedSpec) {
              if (spec_id === item.id) {
                specName.push(item.name)
              }
            }
          }
          this.$emit('confirm', this.checkedSpec, specName);
        } else {
          this.$emit('confirm', [], []);
        }
      },
    },
    watch: {
      visible(visible) {
        if (visible && this.checkedSpec && this.checkedSpec.length > 0) {
          for (let specCls of this.specClsItems) {
            for (let spec of specCls.spec_list) {
              if (spec.id === this.checkedSpec[0]) {
                this.selectedSpecCls = specCls;
                this.specClsId = specCls.id;
                return
              }
            }
          }
        }
      },
    },
  }
</script>