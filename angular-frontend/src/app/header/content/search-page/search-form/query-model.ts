export class QueryModel {
  constructor(public director: string,
              public writer: string,
              public genres: string[],
              public min_rating_imdb: number,
              public year_from: number,
              public year_to: number,
              public principals: string[],
              public title: string,
              public page_size: number,
              public current_page: number,
              public sort_by: string
  ) {
  }

  public clone(): QueryModel {
    return new QueryModel(this.director, this.writer, Object.assign([], this.genres),
      this.min_rating_imdb, this.year_from, this.year_to, Object.assign([], this.principals),
      this.title, this.page_size, this.current_page, this.sort_by)
  }
}
