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

  constructor(private queryService: QueryService) {
    this.pages = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
  }

  ngOnInit() {
    this.queryService.new_query$.subscribe(is_new_query => {
      if (is_new_query) this.current_page = 1
    })
  }

  onClickPageNr(page: number) {
    this.current_page = page;
    this.loadNewPage();
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

}
