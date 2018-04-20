export class SearchModel {
  constructor(public director: string,
              public writer: string,
              public genres: string[],
              public minRatingIMDB: number,
              public year_from: number,
              public year_to: number,
              public principals: string[],
              public title: string,
              public page_size: number,
              public currentPage: number,
              public sortBy: string
  ) {
  }

  public clone(): SearchModel {
    return new SearchModel(this.director, this.writer, Object.assign([], this.genres),
      this.minRatingIMDB, this.year_from, this.year_to, Object.assign([], this.principals),
      this.title, this.page_size, this.currentPage, this.sortBy)
  }
}
