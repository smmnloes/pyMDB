import {Component, OnInit} from '@angular/core';
import {QueryService} from "../../../query.service";

@Component({
  selector: 'app-search-results',
  templateUrl: './search-results.component.html',
  styleUrls: ['./search-results.component.css']
})
export class SearchResultsComponent implements OnInit {


  constructor(private queryService: QueryService) {

  }

  results: any[];

  ngOnInit() {

    this.queryService.result$.subscribe(data => {
      console.log(data);
      this.results = data;
    })
  }

}
