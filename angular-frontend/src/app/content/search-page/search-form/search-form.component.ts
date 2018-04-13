import {Component, Input, OnInit} from '@angular/core';
import {SearchModel} from "./search-model";
import {QueryService} from "../../../query.service";

@Component({
  selector: 'app-search-form',
  templateUrl: './search-form.component.html',
  styleUrls: ['./search-form.component.css']
})
export class SearchFormComponent implements OnInit {
  searchModel: SearchModel;

  @Input()
  genres: string[];

  constructor(private queryService: QueryService) {
  }

  ngOnInit() {
    this.searchModel = new SearchModel("", "", [], null,
      null, null, ["", "", ""]);
  }

  onSubmit() {
    this.queryService.makeQuery(this.searchModel);
  }

}
