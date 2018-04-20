import {Component, OnInit} from '@angular/core';
import {QueryService} from "../../../query.service";

@Component({
  selector: 'app-search-results',
  templateUrl: './search-results.component.html',
  styleUrls: ['./search-results.component.css']
})
export class SearchResultsComponent implements OnInit {
  nr_of_results:number;

  constructor(private queryService: QueryService) {

  }

  results: any[];

  ngOnInit() {

    this.queryService.result$.subscribe(data => {
      console.log(data);
      this.results = data;
    });
    this.queryService.nr_results$.subscribe(nr_of_results=>{
      console.log("Recieved results!");
      this.nr_of_results = nr_of_results;
    })
  }

}
