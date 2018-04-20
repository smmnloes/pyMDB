import {Component, Input, OnInit} from '@angular/core';
import {QueryService} from "../../../../query.service";

@Component({
  selector: 'app-pagination',
  templateUrl: './pagination.component.html',
  styleUrls: ['./pagination.component.css']
})
export class PaginationComponent implements OnInit {
  @Input()
  current_page: number;
  pages: number[];
  nr_of_results: number;
  max_nr_pages:number;

  constructor(private queryService: QueryService) {
    this.pages = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
  }

  ngOnInit() {
    // this.current_page = 1;
    this.queryService.new_query$.subscribe(is_new_query => {
      if (is_new_query) this.current_page = 1
    });
    this.queryService.nr_results$.subscribe(nr_results => {
      this.nr_of_results = nr_results;
      this.max_nr_pages = Math.ceil(nr_results / this.queryService.PAGE_SIZE);
    })
  }

  onClickPageNr(new_page: number) {
    if (this.current_page != new_page) {
      this.current_page = new_page;
      this.loadNewPage();
    }
  }

  onClickNext() {
    this.current_page++;
    this.loadNewPage();
  }

  onClickPrev() {
    this.current_page--;
    this.loadNewPage();
  }

  loadNewPage() {
    this.queryService.loadPage(this.current_page);
  }

  resultsAvailable() {
    return this.queryService.lastQuery != null;
  }

  onClickFirst() {
    this.current_page = 1;
    this.loadNewPage();
  }

  getPages() {
    let pages: number[] = [];
    let lower_limit = this.current_page > 5 ? this.current_page - 5 : 1;
    let upper_limit = (this.current_page > 5 ? this.current_page + 4 : 10);
    if (upper_limit > this.max_nr_pages) {
      upper_limit = this.max_nr_pages;
    }

    for (let i = lower_limit; i <= upper_limit; i++) {
      pages.push(i);
    }

    return pages;
  }

}
