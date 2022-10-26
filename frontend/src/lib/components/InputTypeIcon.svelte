<script>
    import IconText from '~icons/lucide/text-cursor-input';
    import IconSelect from '~icons/mdi/form-dropdown';
    import IconRadio from '~icons/fontisto/radio-btn-active';
    import IconCheckbox from '~icons/fluent/checkbox-checked-24-filled';
    import IconDatePicker from '~icons/uiw/date';
    import IconTextArea from '~icons/bi/textarea-t';
    
    let iconMapping = [
		{ field_type: 'Text',   component: IconText   },
		{ field_type: 'Select', component: IconSelect },
		{ field_type: 'Radio', component: IconRadio },
		{ field_type: 'Checkbox',  component: IconCheckbox  },
		{ field_type: 'Date Picker',  component: IconDatePicker  },
		{ field_type: 'Text Area',  component: IconTextArea  }
    ]

    export let inputType;

</script>

<svelte:component this={iconMapping[iconMapping.findIndex(iconMap => iconMap.field_type === inputType)].component}/>
