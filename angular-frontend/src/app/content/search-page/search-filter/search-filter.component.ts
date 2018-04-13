import {Component, Input, OnInit} from '@angular/core';
import {SearchModel} from "./search-model";
import {QueryService} from "../../../query.service";

@Component({
  selector: 'app-search-filter',
  templateUrl: './search-filter.component.html',
  styleUrls: ['./search-filter.component.css']
})
export class SearchFilterComponent implements OnInit {
  searchModel: SearchModel;

  @Input()
  genres: string[];

  constructor(private queryService: QueryService) {
  }

  ngOnInit() {
    this.searchModel = new SearchModel("", "", [], 5.0,
      1900, 2020, ["", "", ""]);
  }

  onSubmit() {
    console.log(this.searchModel);
  }

}
