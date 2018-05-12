import {Component, forwardRef, OnInit} from '@angular/core';
import {ControlValueAccessor, NG_VALUE_ACCESSOR} from "@angular/forms";
import {imdbGenres} from "./IMDBgenres";

@Component({
  selector: 'app-multiselect',
  exportAs: 'multiselect',
  templateUrl: './multiselect.component.html',
  styleUrls: ['./multiselect.component.css'],

  providers: [
    {
      provide: NG_VALUE_ACCESSOR,
      useExisting: forwardRef(() => MultiselectComponent),
      multi: true
    }
  ]
})
export class MultiselectComponent implements OnInit, ControlValueAccessor {
  dropdownList = [];
  selectedItems = [];
  dropdownSettings = {};
  MAX_NUMBER_SELECTION = 3;

  constructor() {
  }

  ngOnInit() {
    this.dropdownList = imdbGenres.genres;

    this.selectedItems = [];

    this.dropdownSettings = {
      singleSelection: false,
      text: `Select Genres (max. ${this.MAX_NUMBER_SELECTION})`,
      selectAllText: 'Select All',
      unSelectAllText: 'UnSelect All',
      enableSearchFilter: true,
      classes: "myclass custom-class",
      enableCheckAll: false
    };
  }


  onItemSelect(item: any) {
    if (this.selectedItems.length > this.MAX_NUMBER_SELECTION) {
      let i = 0;
      let new_array = [];
      while (i < this.MAX_NUMBER_SELECTION) {
        new_array[i] = this.selectedItems[i];
        i++;
      }
      this.selectedItems = new_array;
    }

    this.propagate();
  }

  onItemDeselect(item: any) {
    this.propagate();
  }

  propagate() {
    let onlyNames = this.selectedItems.map(item => item['itemName']);
    this.propagateChange(onlyNames);
  }

  propagateChange = (_: any) => {
  };

  registerOnChange(fn) {
    this.propagateChange = fn;
  }

  registerOnTouched() {
  }

  writeValue(values: any) {
    let selectedItemsNew = [];
    if (values != null) {
      for (let value of values) {
        for (let option of this.dropdownList) {
          if (option.itemName == value) {
            selectedItemsNew.push(option);
          }
        }
      }
    }
    this.selectedItems = selectedItemsNew;
  }
}
