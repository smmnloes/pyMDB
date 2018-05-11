export class QueryModel {
  constructor(public director: string,
              public writer: string,
              public genres: string[],
              public min_rating_imdb: number,
              public year_from: number,
              public year_to: number,
              public principals: string[],
              public title: string,
              public results_per_page: number,
              public current_page: number,
              public sort_by: string
  ) {
  }

  public clone(): QueryModel {
    return new QueryModel(this.director, this.writer, Object.assign([], this.genres),
      this.min_rating_imdb, this.year_from, this.year_to, Object.assign([], this.principals),
      this.title, this.results_per_page, this.current_page, this.sort_by)
  }

  public static fromQueryParams(queryParams: any) {
    return new QueryModel(
      queryParams.director == null ? "" : queryParams.director,
      queryParams.writer == null ? "" : queryParams.writer,
      queryParams.genres == null ? [] : queryParams.genres,
      queryParams.min_rating_imdb == null ? null : queryParams.min_rating_imdb,
      queryParams.year_from == null ? null : queryParams.year_from,
      queryParams.year_to == null ? null : queryParams.year_to,
      queryParams.principals == null ? ["", "", ""] : queryParams.principals,
      queryParams.title == null ? "" : queryParams.title,
      queryParams.results_per_page,
      queryParams.current_page == null ? 1 : queryParams.current_page,
      queryParams.sort_by == null ? 'Title' : queryParams.sort_by
    )
  }
}
