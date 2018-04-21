import {Component, OnInit} from '@angular/core';
import {QueryService} from "../../../../query.service";

@Component({
  selector: 'app-pagination',
  templateUrl: './pagination.component.html',
  styleUrls: ['./pagination.component.css']
})
export class PaginationComponent implements OnInit {
  private currentPage: number;
  private resultCount: number;
  private maxPageCount: number;

  constructor(private queryService: QueryService) {
  }

  ngOnInit() {
    this.queryService.newQuery$.subscribe(isNewQuery => {
      if (isNewQuery) this.currentPage = 1
    });
    this.queryService.resultCount$.subscribe(resultCount => {
      this.resultCount = resultCount;
      this.maxPageCount = Math.ceil(<number>resultCount / this.queryService.PAGE_SIZE);
    })
  }

  onClickPageNr(newPage: number) {
    if (this.currentPage != newPage) {
      this.currentPage = newPage;
      this.loadNewPage();
    }
  }

  onClickNext() {
    if (this.currentPage < this.maxPageCount) {
      this.currentPage++;
      this.loadNewPage();
    }
  }

  onClickPrev() {
    if (this.currentPage > 1) {
      this.currentPage--;
      this.loadNewPage();
    }
  }

  loadNewPage() {
    this.queryService.loadPage(this.currentPage);
  }

  resultsAvailable() {
    return this.queryService.lastQuery != null;
  }

  onClickFirst() {
    if (this.currentPage != 1) {
      this.currentPage = 1;
      this.loadNewPage();
    }
  }

  onClickLast() {
    if (this.currentPage != this.maxPageCount) {
      this.currentPage = this.maxPageCount;
      this.loadNewPage();
    }
  }

  getPages() {
    let pages: number[] = [];
    let minPage = this.currentPage > 5 ? this.currentPage - 5 : 1;
    let maxPage = (this.currentPage > 5 ? this.currentPage + 4 : 10);

    maxPage = maxPage > this.maxPageCount ? this.maxPageCount : maxPage;

    for (let i = minPage; i <= maxPage; i++) {
      pages.push(i);
    }

    return pages;
  }

}
